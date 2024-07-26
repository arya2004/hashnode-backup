---
title: "Mastering Formatted and File I/O in Go"
seoTitle: "Formatted and File I/O in Go"
seoDescription: "Mastering Formatted and File I/O in Go"
datePublished: Mon Jul 22 2024 19:54:05 GMT+0000 (Coordinated Universal Time)
cuid: clyxenlx9000708krgnf6dowl
slug: mastering-formatted-and-file-io-in-go
cover: https://cdn.hashnode.com/res/hashnode/image/upload/v1721677025638/b3c5ca40-18c6-4000-a32e-3c65dcda1621.jpeg
tags: golang, stream, files

---

In this blog, we'll delve into the world of formatted and file I/O in Go. We'll explore the powerful `fmt` package for formatted I/O and the `os` and `io` packages for file operations. Along the way, we'll demonstrate these concepts with plenty of code examples to illustrate how they work and why they're useful.

## Standard I/O Streams in Go

Go, like many modern programming languages, provides access to standard I/O streams: standard input, standard output, and standard error. These are exposed via the `os` package as `os.Stdin`, `os.Stdout`, and `os.Stderr`. Let's start by understanding the basic usage of these streams.

![](https://cdn.hashnode.com/res/hashnode/image/upload/v1721677778741/9e1ac228-c664-4a8b-9572-2bd692d66b93.png align="center")

### Printing to Standard Output

The `fmt` package provides several functions for printing to the console. The most basic is `fmt.Println`, which prints its arguments followed by a newline. For more control over formatting, we use `fmt.Printf`.

```go
package main

import (
    "fmt"
    "os"
)

func main() {
    fmt.Println("This is printed to standard output.")

    // Using Printf for formatted output
    name := "Alice"
    age := 30
    fmt.Printf("Name: %s, Age: %d\n", name, age)

    // Redirecting output to standard error
    fmt.Fprintf(os.Stderr, "This is an error message.\n")
}
```

### Formatting Strings with `fmt`

The `fmt` package includes functions like `fmt.Sprintf`, which returns a formatted string instead of printing it. This is useful when you need to store the formatted string for later use.

```go
func main() {
    name := "Alice"
    age := 30
    formattedString := fmt.Sprintf("Name: %s, Age: %d", name, age)
    fmt.Println(formattedString)
}
```

### Formatting Verbs in Go

Formatting verbs in Go are placeholders within a format string. Here are some common verbs:

* `%s`: String
    
* `%d`: Decimal integer
    
* `%x`: Hexadecimal integer
    
* `%f`: Floating point
    
* `%t`: Boolean
    
* `%v`: Default format
    

![](https://cdn.hashnode.com/res/hashnode/image/upload/v1721677830427/fbd46a95-2510-482e-af6c-41b9c25df7c4.png align="center")

```go
func main() {
    // Formatting integers
    number := 255
    fmt.Printf("Decimal: %d, Hex: %x, Binary: %b\n", number, number, number)

    // Formatting floating-point numbers
    pi := 3.14159
    fmt.Printf("Default float: %f, Two decimals: %.2f\n", pi, pi)

    // Formatting booleans and generic values
    isTrue := true
    fmt.Printf("Boolean: %t, Generic: %v\n", isTrue, isTrue)
}
```

## File I/O in Go

File I/O in Go is straightforward with the `os` package. Let's start with reading files.

![](https://cdn.hashnode.com/res/hashnode/image/upload/v1721677859182/9e7a3766-7b41-46e1-a5f4-f0c96c5f84d9.png align="center")

### Reading Files

To read a file, we use [`os.Open`](http://os.Open) to get a file handle and `bufio.NewScanner` to read it line by line.

```go
package main

import (
    "bufio"
    "fmt"
    "os"
)

func main() {
    file, err := os.Open("example.txt")
    if err != nil {
        fmt.Fprintf(os.Stderr, "Error opening file: %v\n", err)
        return
    }
    defer file.Close()

    scanner := bufio.NewScanner(file)
    for scanner.Scan() {
        fmt.Println(scanner.Text())
    }

    if err := scanner.Err(); err != nil {
        fmt.Fprintf(os.Stderr, "Error reading file: %v\n", err)
    }
}
```

### Writing Files

To write to a file, we use `os.Create` to create or truncate the file, and `fmt.Fprintf` to write to it.

```go
func main() {
    file, err := os.Create("output.txt")
    if err != nil {
        fmt.Fprintf(os.Stderr, "Error creating file: %v\n", err)
        return
    }
    defer file.Close()

    fmt.Fprintf(file, "This is a line of text.\n")
    fmt.Fprintf(file, "This is another line of text.\n")
}
```

### Using `io/ioutil` for Simple File Operations

The `io/ioutil` package provides convenient functions for simple file operations, like reading an entire file into memory.

```go
package main

import (
    "fmt"
    "io/ioutil"
    "os"
)

func main() {
    data, err := ioutil.ReadFile("example.txt")
    if err != nil {
        fmt.Fprintf(os.Stderr, "Error reading file: %v\n", err)
        return
    }
    fmt.Println(string(data))

    err = ioutil.WriteFile("output.txt", data, 0644)
    if err != nil {
        fmt.Fprintf(os.Stderr, "Error writing file: %v\n", err)
    }
}
```

## Building a Simple `cat` Program

Let's combine these concepts to build a simple version of the Unix `cat` command, which reads files and prints their contents to standard output.

```go
package main

import (
    "fmt"
    "io"
    "os"
)

func main() {
    if len(os.Args) < 2 {
        fmt.Fprintf(os.Stderr, "Usage: %s <file1> <file2> ...\n", os.Args[0])
        os.Exit(1)
    }

    for _, filename := range os.Args[1:] {
        file, err := os.Open(filename)
        if err != nil {
            fmt.Fprintf(os.Stderr, "Error opening file %s: %v\n", filename, err)
            continue
        }

        if _, err := io.Copy(os.Stdout, file); err != nil {
            fmt.Fprintf(os.Stderr, "Error reading file %s: %v\n", filename, err)
        }

        file.Close()
    }
}
```

## Building a Word Count Program

We'll now create a program that mimics the Unix `wc` command, counting lines, words, and characters in a file.

```go
package main

import (
    "bufio"
    "fmt"
    "os"
    "strings"
)

func main() {
    if len(os.Args) < 2 {
        fmt.Fprintf(os.Stderr, "Usage: %s <file1> <file2> ...\n", os.Args[0])
        os.Exit(1)
    }

    for _, filename := range os.Args[1:] {
        file, err := os.Open(filename)
        if err != nil {
            fmt.Fprintf(os.Stderr, "Error opening file %s: %v\n", filename, err)
            continue
        }

        lines, words, chars := 0, 0, 0
        scanner := bufio.NewScanner(file)
        for scanner.Scan() {
            lines++
            text := scanner.Text()
            words += len(strings.Fields(text))
            chars += len(text)
        }

        if err := scanner.Err(); err != nil {
            fmt.Fprintf(os.Stderr, "Error reading file %s: %v\n", filename, err)
        }

        fmt.Printf("%d %d %d %s\n", lines, words, chars, filename)
        file.Close()
    }
}
```

In this post, we've covered the basics of formatted and file I/O in Go. We explored the `fmt` package for printing and formatting strings and the `os` and `io` packages for file operations. We also built simple versions of the Unix `cat` and `wc` commands to demonstrate these concepts in action. With these tools, you can handle a wide range of I/O tasks in your Go programs.