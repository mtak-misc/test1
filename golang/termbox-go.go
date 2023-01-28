package main

import (
    "github.com/nsf/termbox-go"
)

var todos = []string{"Buy milk", "Walk the dog", "Write a letter"}

func main() {
    err := termbox.Init()
    if err != nil {
        panic(err)
    }
    defer termbox.Close()

    eventQueue := make(chan termbox.Event)
    go func() {
        for {
            eventQueue <- termbox.PollEvent()
        }
    }()

    selected := 0
    running := true
    for running {
        drawTodos(selected)
        switch ev := <-eventQueue; ev.Type {
        case termbox.EventKey:
            switch ev.Key {
            case termbox.KeyArrowUp:
                selected--
                if selected < 0 {
                    selected = len(todos) - 1
                }
            case termbox.KeyArrowDown:
                selected++
                if selected >= len(todos) {
                    selected = 0
                }
            case termbox.KeyEnter:
                todos = append(todos[:selected], todos[selected+1:]...)
                selected--
                if selected < 0 {
                    selected = 0
                }
            case termbox.KeyEsc:
                running = false
            }
        }
    }
}

func drawTodos(selected int) {
    termbox.Clear(termbox.ColorDefault, termbox.ColorDefault)
    for i, todo := range todos {
        color := termbox.ColorDefault
        if i == selected {
            color = termbox.ColorGreen
        }
        termbox.SetCell(1, i+1, ' ', color, termbox.ColorDefault)
        termbox.SetCell(2, i+1, ' ', color, termbox.ColorDefault)
        for j, char := range todo {
            termbox.SetCell(3+j, i+1, char, color, termbox.ColorDefault)
        }
    }
    termbox.Flush()
}
