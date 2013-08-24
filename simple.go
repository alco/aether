package main

import (
    "bufio"
    "fmt"
    "os"
    "unicode/utf8"
)

func main() {
    r := bufio.NewReader(os.Stdin)
    line, _, _ := r.ReadLine()

    length := utf8.RuneCount(line)
    runes := make([]rune, 0, length)
    offs := 0
    for offs < len(line) {
        r, size := utf8.DecodeRune(line[offs:])
        runes = append(runes, r)
        offs += size
    }
    for i := 0; i < length/2; i++ {
        runes[i], runes[length-i-1] = runes[length-i-1], runes[i]
    }

    final_line := string(runes)
    fmt.Println(final_line)
}


///////////////////////////


// import io
//
// fn main() {
//     io.readln() => reverse => print
// }

