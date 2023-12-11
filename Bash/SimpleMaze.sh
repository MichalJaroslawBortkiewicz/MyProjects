#!/bin/bash

declare -A maze

clear

read -r rows cols < <(stty size)
cols=$((cols / 2))
#rows=23
#cols=23

if [[ $((cols % 2)) == 0 ]]; then
    cols=$((cols - 1))
fi

if [[ $((rows % 2)) == 0 ]]; then
    rows=$((rows - 1))
fi


start_x=2
start_y=2

uw_lines=0
escape_char=$(printf "\u1b")


x_free_spaces=()
y_free_spaces=()

x_directions=("0" "2" "0" "-2")
y_directions=("2" "0" "-2" "0")

initialize_maze() {
    for ((i = 0; i < rows + 2; i++)); do
        for ((j = 0; j < cols + 2; j++)); do
            maze[$i,$j]='#'
        done
    done
}

carve_path() {
    local x=$1
    local y=$2

    directions_ind=("0" "1" "2" "3")
    shuf_directions=($(shuf -e -- "${directions_ind[@]}"))

    for d in "${shuf_directions[@]}"; do
        dx="${x_directions[d]}"
        dy="${y_directions[d]}"

        nx=$((x + dx))
        ny=$((y + dy))


        if [[ $nx -gt 1 && $nx -le $rows && $ny -gt 1 && $ny -le $cols && "${maze[$nx,$ny]}" == "#" ]]; then
            cx=$((x + dx/2))
            cy=$((y + dy/2))
            maze[$cx,$cy]=' '
            maze[$nx,$ny]=' '
            x_free_spaces+=("${cx} ")
            x_free_spaces+=("${nx} ")
            y_free_spaces+=("${cy} ")
            y_free_spaces+=("${ny} ")
            carve_path $nx $ny
        fi
    done
}

print_maze() {
    for ((j = 1; j <= cols; j++)); do
        echo -n "${maze[1,$j]} "
    done
    for ((i = 2; i <= rows; i++)); do
        echo
        for ((j = 1; j <= cols; j++)); do
            echo -n "${maze[$i,$j]} "
        done
    done
}

initialize_prog() {
    initialize_maze
    maze[1,2]=' '

    carve_path $start_x $start_y

    x_free_spaces_shuffled=($(shuf -e -- "${x_free_spaces[@]}"))
    n="${#x_free_spaces[@]}"

    array_inds=($(seq 0 1 $((n - 1))))
    shuf_array_inds=($(shuf -e -- "${array_inds[@]}"))

    chosen_number="${shuf_array_inds[0]}"
    px=$(( x_free_spaces[chosen_number] ))
    py=$(( y_free_spaces[chosen_number] ))

    print_maze
    printf "\033[%d;%dH O\033[0;0H" $(( py + uw_lines )) $(( 2 * px - 2 ))
}

main() {
    initialize_prog

    while true; do
        printf "\033[0;0H"
        read -rsn1 mode # get 1 character
        if [[ $mode == $escape_char ]]; then
            read -rsn2 mode # read 2 more chars
        fi
        case $mode in
            'q') exit ;;
            '[A') ny=$((py - 1)); nx=$px; ;;
            '[B') ny=$((py + 1)); nx=$px; ;;
            '[D') nx=$((px - 1)); ny=$py; ;;
            '[C') nx=$((px + 1)); ny=$py; ;;
            *) >&2 continue;;
        esac


        if [[ "${maze[$ny,$nx]}" == "#" ]]; then
            continue;
        fi

        printf "\033[%d;%dH  \033[0;0H" $(( py + uw_lines )) $(( 2 * (px - 1) ))

        px=$nx
        py=$ny

        printf "\033[%d;%dH O\033[0;0H" $(( py + uw_lines )) $(( 2 * (px - 1) ))
    done

}


main