package main

// go-winres simply --icon icon.png --manifest gui
// go build -ldflags="-H windowsgui"

import (
	"log"
	"os/exec"

	"github.com/fsnotify/fsnotify"
)

func main() {
	watcher, err := fsnotify.NewWatcher()
	if err != nil {
		log.Fatal(err)
	}
	defer watcher.Close()

	done := make(chan bool)
	go func() {
		for {
			select {
			case event, ok := <-watcher.Events:
				if !ok {
					return
				}
				// log.Println("event:", event)
				if event.Op&fsnotify.Write == fsnotify.Write {
					// log.Println("modified file:", event.Name)
					cmd := exec.Command("./py/pythonw.exe", "main.py")

					cmd.Start()
				}
				break
			case err, ok := <-watcher.Errors:
				if !ok {
					return
				}
				log.Println("error:", err)
				break
			}
		}
	}()

	err = watcher.Add("todo.txt")
	if err != nil {
		log.Fatal(err)
	}
	<-done
}
