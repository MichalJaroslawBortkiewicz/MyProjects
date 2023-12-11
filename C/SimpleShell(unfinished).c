#define _POSIX_SOURCE

#include <signal.h>
#include <stdio.h>
#include <stdlib.h>
#include <stdbool.h>
#include <string.h>
#include <sys/types.h>
#include <sys/wait.h>
#include <unistd.h>


#define MAX_INPUT_SIZE 1024
#define MAX_COMMAND_SIZE 128
#define MAX_ARG_SIZE 64
#define MAX_COMMANDS 16
#define MAX_JOBS 10

#define RED "\x1b[31m]"
#define GREEN "\x1b[32m"
#define BLUE "\x1b[34m"
#define COLOR_RESET "\x1b[39m"

#define BOLD_TEXT "\x1b[1m"
#define TEXT_RESET "\x1b[0m"


typedef struct {
    pid_t pid;
    char command[MAX_COMMAND_SIZE];
} Job;

typedef struct {
    int no_args;
    bool redirect;
    char *args[MAX_COMMAND_SIZE];
} Command;


Job jobs[MAX_JOBS];
int job_count = 0;


char *stdcommands[] = {"cd", "ls", "jobs", "bg", "fg", "kill", "exit"}; //"mkdir"

int no_current_pids = 0;
pid_t current_pids[MAX_JOBS];

void sigchld_handler(int signo) {
    (void)signo;
    while (waitpid(-1, NULL, WNOHANG) > 0);
}

void sigint_handler(int signo) {
    (void)signo;
    printf("\n");

    for(int i = 0; i < no_current_pids; i++){
        kill(current_pids[i], SIGINT);
    }

    no_current_pids = 0;
}

void add_job(pid_t pid, const char *command) {
    if (job_count < MAX_JOBS) {
        jobs[job_count].pid = pid;
        strncpy(jobs[job_count].command, command, MAX_INPUT_SIZE);
        jobs[job_count].command[MAX_INPUT_SIZE - 1] = '\0';
        job_count++;
    } else {
        printf("Error: Maximum number of jobs reached.\n");
    }
}


void display_jobs() {
    printf("Jobs:\n");
    for (int i = 0; i < job_count; i++) {
        printf("[%d] %s\n", i + 1, jobs[i].command);
    }
}


void kill_process(int job_number) {
    if (job_number > 0 && job_number <= job_count) {
        pid_t proc_pid = jobs[job_number - 1].pid;

        kill(proc_pid, SIGKILL);
        printf("[%d] %s terminated.\n", job_number, jobs[job_number - 1].command);
    } else {
        printf("Error: Invalid job number.\n");
    }
}



void execute_commands(Command **commands, int no_commands, bool background){
    if(no_commands == 0){return;}
    if(no_commands == 1){
        pid_t pid = fork();
        char **args = commands[0]->args;

        if (pid == 0) {
            current_pids[no_current_pids++] = execvp(args[0], args);
        }

        waitpid(current_pids[no_current_pids - 1], NULL, 0);
        no_current_pids = 0;
        return;
    }

    int pipe_fd[2];
    int temp_pipe;

    for(int i = 0; i < no_commands; i++){
        char **args = commands[i]->args;
        
        if(i < no_commands - 1){ pipe(pipe_fd); }

        pid_t pid = fork();

        if (pid == 0) {
            if (i > 0){
                close(0);
                dup(temp_pipe);
                close(temp_pipe);
            }

            if(i < no_commands - 1){
                close(1);
                dup(pipe_fd[1]);
            }
            

            close(pipe_fd[0]);
            close(pipe_fd[1]);


            current_pids[no_current_pids++] = execvp(args[0], args);
            perror("lsh");
            exit(EXIT_FAILURE);
        } else if (pid > 0 && background) {
            add_job(pid, args[0]);
            printf("[%d] %s running in background.\n", job_count, args[0]);


        } else if (pid < 0){
            perror("lsh");
        }

        if(i > 0){
            close(temp_pipe);
        }
        close(pipe_fd[1]);

        temp_pipe = pipe_fd[0];

    }

    waitpid(current_pids[no_current_pids - 1], NULL, 0);
    no_current_pids = 0;

}


void parse_command(char *input, char **args, int *no_args) {
    /* if (strncmp(input, "ls", 2)){
        strcat(input, " --color");
    } */

    int arg_count = 0;
    char *save_token;
    char *token = strtok_r(input, " \t\n", &save_token);
    while (token != NULL && arg_count < MAX_ARG_SIZE - 1) {
        if(token)

        args[arg_count++] = token;
        token = strtok_r(NULL, " \t\n", &save_token);
    }
    args[arg_count] = NULL;
    *no_args = arg_count;
}


int divide_commands(char *input, Command **commands){
    int command_count = 0;

    char *save_token;
    char *token = strtok_r(input, "|", &save_token);
    while (token != NULL && strcmp("", token) != 0 && command_count < MAX_ARG_SIZE - 1) {
        parse_command(token, commands[command_count]->args, &commands[command_count]->no_args);
        token = strtok_r(NULL, "|", &save_token);
        command_count++;
    }

    return command_count;
}



int main() {
    signal(SIGCHLD, sigchld_handler);
    signal(SIGINT, sigint_handler);

    while (1) {

        char input[MAX_INPUT_SIZE];
        Command *commands[MAX_COMMANDS];

        bool background  = false;
 
        char current_directory[MAX_INPUT_SIZE];
        if (getcwd(current_directory, sizeof(current_directory)) != NULL) {
            printf("%s%s%slsh%s:%s~%s%s$ ", BOLD_TEXT, GREEN, TEXT_RESET, BOLD_TEXT, BLUE, current_directory, TEXT_RESET);
        } else {
            perror("lsh");
            printf("%s%slsh%s:$ ", BOLD_TEXT, GREEN, TEXT_RESET);
        }


        char *has_input = fgets(input, MAX_INPUT_SIZE, stdin);

        if (feof(stdin)) {
            printf("exit\n");
            break;
        } else if (has_input == NULL){
            printf("\n");
            continue;
        }
        

        input[strcspn(input, "\n")] = '\0';

        int pos_to_move = strspn(input, " \t");
        if(pos_to_move > 0){
            memmove(input, input + pos_to_move, strlen(input) - pos_to_move + 1);
        }

        size_t input_len = strlen(input);
        while(input[input_len - 1] == ' '){
            input[--input_len] = '\0';
        }

        if(input[input_len - 1] == '&'){
            input[--input_len] = '\0';
            background = true;
        }

        if (strcmp(input, "exit") == 0) {
            break;
        } else if (strcmp(input, "cd") == 0) {
            char *home = getenv("HOME");
            chdir(home);
            continue;
        } else if (strncmp(input, "jobs", 4) == 0) {
            display_jobs();
            continue;
        } else if (strncmp(input, "fg", 2) == 0) {
            int job_number;
            sscanf(input + 2, "%d", &job_number);
            if (job_number > 0 && job_number <= job_count) {
                waitpid(jobs[job_number - 1].pid, NULL, 0);
            } else {
                printf("Error: Invalid job number.\n");
            }
            continue;
        } else if (strncmp(input, "bg", 2) == 0) {
            int job_number;
            sscanf(input + 2, "%d", &job_number);
            if (job_number > 0 && job_number <= job_count) {
                kill(jobs[job_number - 1].pid, SIGCONT);
            } else {
                printf("Error: Invalid job number.\n");
            }
            continue;
        } else if (strncmp(input, "kill", 4) == 0) {
            int job_number;
            sscanf(input + 5, "%d", &job_number);
            kill_process(job_number);
            continue;
        }


        for (int i = 0; i < MAX_COMMANDS; i++) {
            commands[i] = malloc(sizeof(Command));
        }

        int no_commands = divide_commands(input, commands);

        execute_commands(commands, no_commands, background);


        for (int i = 0; i < no_commands; i++) {
            free(commands[i]);
        }
    }

    return 0;
}