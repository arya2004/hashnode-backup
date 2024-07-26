---
title: "Deep Dive into Go: Control Statements, Packages, Declarations, and Operators"
seoTitle: "Go: Control Statements, Packages, Declarations, and Operators"
seoDescription: "Deep Dive into Go: Control Statements, Packages, Declarations, and Operators"
datePublished: Sat Jul 20 2024 14:33:24 GMT+0000 (Coordinated Universal Time)
cuid: clyu8bhy3000709l78on6emks
slug: deep-dive-into-go-control-statements-packages-declarations-and-operators
cover: https://cdn.hashnode.com/res/hashnode/image/upload/v1721484205398/2b9270ba-0c36-4815-b1dc-d323af637c53.png
tags: go, operators, conditional-statement

---

We’ve touched on these topics before, but let’s circle back and explore them in greater detail. Specifically, we'll look at control statements, packages, declarations, and operators. Buckle up, it’s gonna be fun!

## Control Structures in Go

### If Statements

The `if` statement is a basic control structure in Go. One thing to note is that braces `{}` are mandatory, even if you have a single statement inside the `if`. Here's a basic example:

```go
if condition {
    // your code here
}
```

This is not a choice; you can't skip the braces. The braces have to be laid out in the Launcher Base Style (1TBS), which is enforced by the compiler.

You can also have a short variable declaration in the `if` statement, like this:

```go
if err := someFunction(); err != nil {
    // handle error
}
```

Here, `err` is declared and assigned the result of `someFunction()`, and then checked for the condition `err != nil`.

### For Loops

Go only has one looping construct, the `for` loop. It can be used in several ways:

1. **Classic for loop:**
    

```go
for i := 0; i < 10; i++ {
    fmt.Println(i)
}
```

This loop has three parts separated by semicolons:

* Initialization (`i := 0`)
    
* Condition (`i < 10`)
    
* Post iteration increment (`i++`)
    

2. **While loop (kind of):**
    

```go
for condition {
    // your code here
}
```

This behaves like a `while` loop found in other languages.

3. **Infinite loop:**
    

```go
for {
    // your code here
}
```

This starts an infinite loop which continues until you explicitly break out of it.

4. **Range loop:**
    

```go
// Iterating over a slice
slice := []int{1, 2, 3}
for i, v := range slice {
    fmt.Println(i, v)
}

// Iterating over a map
myMap := map[string]int{"a": 1, "b": 2}
for k, v := range myMap {
    fmt.Println(k, v)
}
```

The `range` operator returns one or two values. For slices, it returns the index and the value at that index. For maps, it returns the key and the value for that key. One important detail is that the value is copied, which is efficient for small types but might not be for larger types.

![](https://cdn.hashnode.com/res/hashnode/image/upload/v1721485260452/983b52a1-8166-4e23-99ee-25e6a28a1dc5.png align="center")

### Switch Statements

Switch statements in Go are a cleaner way to handle multiple conditions. They break automatically after each case, unlike in some other languages where you need a `break` statement.

```go
switch day {
case "Monday":
    fmt.Println("Start of the week!")
case "Friday":
    fmt.Println("Almost weekend!")
default:
    fmt.Println("Just another day")
}
```

Switch cases are evaluated from top to bottom, and the `default` case is evaluated last no matter where it is placed in the switch statement.

You can also switch on true for more complex conditions:

```go
switch {
case age < 18:
    fmt.Println("Minor")
case age >= 18 && age < 60:
    fmt.Println("Adult")
default:
    fmt.Println("Senior")
}
```

This form of the switch statement is like a series of `if-else` statements.

## Packages

Every Go file belongs to a package. The main package is special because it defines the entry point for the executable:

```go
package main

import "fmt"

func main() {
    fmt.Println("Hello, Go!")
}
```

Packages help in organizing code and managing dependencies. Here’s how you import a package:

```go
import "fmt"
```

You can have multiple files in a package, and each file must import the necessary dependencies individually.

### Exported vs Unexported Identifiers

In Go, if an identifier (variable, type, function, etc.) starts with a capital letter, it is exported and can be accessed from other packages. If it starts with a lowercase letter, it is unexported and private to the package.

```go
// In package mypackage
var ExportedVar = "I can be accessed from other packages"
var unexportedVar = "I am private to mypackage"
```

## Declarations

Go supports different kinds of declarations, including constants, types, and variables.

![](https://cdn.hashnode.com/res/hashnode/image/upload/v1721485347814/d76a7d54-583c-434b-8237-cff3b509eef7.png align="center")

### Variable Declarations

Variables can be declared using the `var` keyword or the short declaration `:=`:

```go
var a int = 10
b := 20
```

You can also declare multiple variables in a block:

```go
var (
    x int
    y = 20
    z int = 30
)
```

![](https://cdn.hashnode.com/res/hashnode/image/upload/v1721485416942/d80daef0-871a-46bc-a8bf-2fb6dc811770.png align="center")

### Short Declaration Operator

The short declaration `:=` can only be used within functions:

```go
func main() {
    a := 10
    fmt.Println(a)
}
```

It’s also the only way to declare a variable at the beginning of a control structure like `if`:

```go
if a := someFunction(); a > 10 {
    fmt.Println("Greater than 10")
}
```

The short declaration operator requires at least one new variable to be declared. If all variables on the left side of `:=` are already declared in the same scope, it will be treated as an assignment.

Here's an example demonstrating a common mistake:

```go
func main() {
    var err error
    // Incorrect usage, redeclaring err
    err := someFunction() // This line will cause a compile error
}
```

To avoid this, you must ensure at least one new variable is introduced:

```go
func main() {
    var err error
    if x, err := someFunction(); err != nil {
        fmt.Println(x)
    }
}
```

### Shadowing

Shadowing occurs when a variable declared in an inner scope has the same name as a variable in an outer scope. Here's an example where shadowing causes a bug:

```go
func main() {
    var err error
    for {
        err := someFunction()
        if err != nil {
            break
        }
    }
    if err != nil {
        fmt.Println("Error occurred")
    }
}
```

In this case, the `err` inside the `for` loop is a different variable from the `err` in the outer scope. The outer `err` remains `nil`, leading to incorrect behavior.

## Types

Go is a statically typed language, meaning variables need to have a type. There are two main typing approaches: structural typing and named typing.

### Structural Typing

![](https://cdn.hashnode.com/res/hashnode/image/upload/v1721485512867/500d6b3f-3759-42af-99f3-ccdd8b8ea6f5.png align="center")

This is based on the structure or behavior of types:

```go
type Person struct {
    Name string
    Age  int
}

var p Person
```

### Named Typing

This is when you explicitly introduce a new type:

```go
type Age int

var myAge Age = 25
var yourAge int = 30

// This won't work
// myAge = yourAge

// You need to convert the type
myAge = Age(yourAge)
```

Named types create distinct types even if they share the same underlying type. This helps in creating more readable and maintainable code by providing context-specific types.

## Operators

Go has a simple set of operators grouped into arithmetic, comparison, and logical operators.

### Arithmetic Operators

```go
a := 10
b := 5

fmt.Println(a + b)  // 15
fmt.Println(a - b)  // 5
fmt.Println(a * b)  // 50
fmt.Println(a / b)  // 2
fmt.Println(a % b)  // 0
```

### Comparison Operators

```go
fmt.Println(a == b) // false
fmt.Println(a != b) // true
fmt.Println(a > b)  // true
fmt.Println(a < b)  // false
fmt.Println(a >= b) // true
fmt.Println(a <= b) // false
```

### Logical Operators

```go
trueVal := true
falseVal := false

fmt.Println(trueVal && falseVal) // false
fmt.Println(trueVal || falseVal) // true
fmt.Println(!trueVal)            // false
```

### Precedence

Operator precedence determines how an expression is evaluated. Use parentheses to make expressions clear:

```go
result := (3 + 4) * 5 // 35
```

## Conclusion

That wraps up our deep dive into some basic Go concepts. We’ve explored control structures, packages, declarations, and operators. This should give you a solid foundation for writing Go programs. In the next segment, we’ll cover I/O and file operations. Stay tuned for more Go goodness!