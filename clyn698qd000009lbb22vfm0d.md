---
title: "Diving Deep into Basic Types in Go"
seoTitle: "Basic Types in Go"
seoDescription: "Diving Deep into Basic Types in Go"
datePublished: Mon Jul 15 2024 16:01:16 GMT+0000 (Coordinated Universal Time)
cuid: clyn698qd000009lbb22vfm0d
slug: diving-deep-into-basic-types-in-go
cover: https://cdn.hashnode.com/res/hashnode/image/upload/v1721056192481/b836ad03-a1b7-4ea2-b969-d582ec9d0aea.png
tags: go, basics

---

# Keywords and Operators in Go

Before we jump into types, let's take a quick look at the keywords and operators in Go. Understanding these will help you grasp the language's syntax and functionality.

![List of 25 Go keywords and various operators and symbols.](https://cdn.hashnode.com/res/hashnode/image/upload/v1721058364866/e2b5fe58-f45a-4e16-bf2b-2f81f3685e49.png align="center")

## Keywords

Go has a surprisingly small set of keywords, which keeps the language simple and easy to understand. Here’s a list of Go keywords:

```go
break       default      func         interface   select
case        defer        go           map         struct
chan        else         goto         package     switch
const       fallthrough  if           range       type
continue    for          import       return      var
```

## Operators

Go operators can be categorized into arithmetic, comparison, logical, bitwise, and others:

### Arithmetic Operators

```go
+    // Addition
-    // Subtraction
*    // Multiplication
/    // Division
%    // Remainder
```

### Comparison Operators

```go
==   // Equal
!=   // Not equal
<    // Less than
<=   // Less than or equal to
>    // Greater than
>=   // Greater than or equal to
```

### Logical Operators

```go
&&   // Logical AND
||   // Logical OR
!    // Logical NOT
```

### Bitwise Operators

```go
&    // AND
|    // OR
^    // XOR
<<   // Left shift
>>   // Right shift
```

### Other Operators

```go
&    // Address of
*    // Pointer dereference
<-   // Send/receive operator for channels
```

## Special Operators

### Assignment Operators

```go
=    // Assignment
+=   // Addition assignment
-=   // Subtraction assignment
*=   // Multiplication assignment
/=   // Division assignment
%=   // Remainder assignment
&=   // AND assignment
|=   // OR assignment
^=   // XOR assignment
<<=  // Left shift assignment
>>=  // Right shift assignment
```

### Increment and Decrement Operators

```go
++   // Increment
--   // Decrement
```

Now that we have an overview of the keywords and operators, let's move on to understanding how Go handles different types of data.

# Numbers in Go vs. Interpreted Languages

One of the first things to understand about Go is how it handles numbers, especially compared to interpreted languages like Python.

![Diagram comparing variable assignment in Go and interpreted languages like Python.](https://cdn.hashnode.com/res/hashnode/image/upload/v1721058465588/51faa217-aac8-4ee0-9726-66d1fb465456.png align="center")

## Interpreted Languages

In languages like Python:

```python
x = 10
```

Here, `x` is an object that represents the number 10. The interpreter takes care of converting this into something the computer understands. Essentially, `x` is not directly a number but an object that the interpreter manages.

### Go

In Go:

```go
var y int = 10
```

`y` is directly a memory location containing the value 10. This direct approach gives Go a performance edge because there's no intermediary interpreter. This difference is fundamental to Go’s type system and performance.

# Basic Integer Types

In Go, the default integer type is `int`. There are also various sized integers, both signed and unsigned, but for most purposes, you’ll use `int`.

![List of Go constants, types, and functions with a note on name shadowing.](https://cdn.hashnode.com/res/hashnode/image/upload/v1721058414983/02953a9f-f813-4f0a-ac6a-11359af60c2e.png align="center")

## Integer Types

Go provides several integer types:

* **int**: Platform-dependent (32-bit or 64-bit)
    
* **int8**: 8-bit signed integer
    
* **int16**: 16-bit signed integer
    
* **int32**: 32-bit signed integer
    
* **int64**: 64-bit signed integer
    
* **uint**: Platform-dependent unsigned integer
    
* **uint8**: 8-bit unsigned integer (alias for byte)
    
* **uint16**: 16-bit unsigned integer
    
* **uint32**: 32-bit unsigned integer
    
* **uint64**: 64-bit unsigned integer
    

### Example

```go
var y int = 10 // Declare an int variable
y := 10       // Short declaration, also creates an int
```

## Float Types

For real numbers (fractions), Go has `float32` and `float64`, with `float64` being the default.

```go
var f float64 = 7.89 // Declare a float64 variable
f := 7.89            // Short declaration, also creates a float64
```

## Type Inference

Go can infer the type of a variable based on its initial value.

```go
var b = 7.89 // Inferred as float64
var i = 10   // Inferred as int
```

## Type Conversion

Go is strict about type conversion. You can’t just mix types without explicitly converting them.

```go
var y int = 15
var b float64 = 15.5

y = int(b) // Convert float64 to int, fractional part is discarded
b = float64(y) // Convert int to float64
```

## Code Example: Playing with Types

Here's a simple program to illustrate the basics of type declarations and conversions.

```go
package main

import (
	"fmt"
)

func main() {
	var y int = 10
	b := 15.5

	fmt.Printf("y: %T, %v\n", y, y)
	fmt.Printf("b: %T, %v\n", b, b)

	y = int(b)
	fmt.Printf("y after conversion: %T, %v\n", y, y)
}
```

Run this in the Go Playground and you'll see how types and conversions work.

# Booleans and Errors

## Boolean Type

Booleans in Go are straightforward—either `true` or `false`.

```go
var isAvailable bool = true
isCompleted := false
```

## Error Type

Errors are a bit more complex but for now, think of them as either `nil` or containing an error message.

```go
var err error = nil
if err != nil {
	fmt.Println("An error occurred")
}
```

# Declarations and Initialization

Go ensures all variables are initialized at declaration, either by you or by default to zero values.

```go
var x int // x is initialized to 0
y := 0    // y is explicitly initialized to 0
```

## Example of Default Initialization

Here's a more detailed example showing default initialization:

```go
package main

import (
	"fmt"
)

func main() {
	var i int
	var f float64
	var b bool
	var s string

	fmt.Printf("%v %v %v %q\n", i, f, b, s)
	// Output: 0 0 false ""
}
```

# Constants

Constants in Go are immutable. They can only be numbers, booleans, or strings.

## Declaring Constants

```go
const pi = 3.14159
const greeting = "Hello, World!"
```

## Using Constants

Constants are evaluated at compile time and can be used in expressions:

```go
const (
	a = 5
	b = 10
	c = a + b // c = 15
)
```

## Practical Example: Calculating Averages

Let's build a simple program to calculate averages from a list of numbers, either from the command line or a file.

```go
package main

import (
	"bufio"
	"fmt"
	"os"
	"strconv"
)

func main() {
	var sum float64
	var count int

	scanner := bufio.NewScanner(os.Stdin)
	for scanner.Scan() {
		val, err := strconv.ParseFloat(scanner.Text(), 64)
		if err != nil {
			fmt.Fprintln(os.Stderr, "Invalid input:", err)
			return
		}
		sum += val
		count++
	}

	if count == 0 {
		fmt.Println("No values provided")
		return
	}

	fmt.Printf("Average: %.2f\n", sum/float64(count))
}
```

### How It Works

1. **Reading Input**: We read input line by line using a scanner.
    
2. **Converting Input**: Each line is converted to a `float64` using `strconv.ParseFloat`.
    
3. **Summing Values**: The values are summed, and the count of inputs is maintained.
    
4. **Calculating Average**: The average is calculated by dividing the sum by the count.
    

You can test this by running the program and providing numbers either directly or through a file.

### Example Usage

#### From the Command Line

```bash
$ go run main.go
8
9
10
Ctrl+D
```

**From a File**

```bash
$ cat numbers.txt
8
9
10

$ go run main.go < numbers.txt
```

# Understanding Strings in Go

## Declaring Strings

Strings in Go are sequences of bytes. Go strings are immutable, meaning once created, they cannot be changed.

```go
var message string = "Hello, World!"
message := "Hello, World!"
```

## String Operations

You can concatenate strings using the `+` operator:

```go
part1 := "Hello, "
part2 := "World!"
message := part1 + part2 // message = "Hello, World!"
```

## String Functions

Go provides a variety of functions for working with strings in the `strings` package:

```go
import (
	"fmt"
	"strings"
)

func main() {
	message := "Hello, World!"
	fmt.Println(strings.ToUpper(message)) // "HELLO, WORLD!"
	fmt.Println(strings.Contains(message, "World")) // true
}
```

# Composite Types: Slices and Maps

## Slices

Slices are a key data type in Go, providing a more powerful interface for sequences than arrays.

```go
var numbers []int // Declare a slice
numbers = append(numbers, 3, 6, 9) // Append values to the slice
```

## Maps

Maps are Go's built-in associative data type (hash table or dictionary).

```go
var ages map[string]int // Declare a map
ages = make(map[string]int) // Initialize the map
ages["Alice"] = 25 // Assign a value
fmt.Println(ages["Alice"]) // Retrieve a value
```

## Example: Using Slices and Maps

Here's a more detailed example demonstrating slices and maps:

```go
package main

import (
	"fmt"
)

func main() {
	// Slices
	numbers := []int{3, 6, 9, 12, 15}
	fmt.Println(numbers)
	numbers = append(numbers, 18)
	fmt.Println(numbers)

	// Maps
	ages := make(map[string]int)
	ages["Charlie"] = 22
	ages["Dana"] = 28
	fmt.Println(ages)
	fmt.Println("Charlie’s age:", ages["Charlie"])
}
```

We've covered the basics of types in Go, including integers, floats, booleans, errors, strings, and composite types like slices and maps. We also touched on variable declarations, type inference, and conversions. By building a simple average calculator and exploring string and composite type operations, we've put these concepts into practice. Next, we'll dive into more advanced topics like functions, methods, and concurrency. Happy coding!