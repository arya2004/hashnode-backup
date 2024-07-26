---
title: "Exploring Built-in Container Types in Go: Arrays, Slices, and Maps"
seoTitle: "Go: Arrays, Slices, and Maps"
seoDescription: "Exploring Built-in Container Types in Go: Arrays, Slices, and Maps"
datePublished: Fri Jul 19 2024 21:11:46 GMT+0000 (Coordinated Universal Time)
cuid: clyt73ytl000608lkfkxo4pi0
slug: exploring-built-in-container-types-in-go-arrays-slices-and-maps
cover: https://cdn.hashnode.com/res/hashnode/image/upload/v1721422070298/3210a242-710d-4fd4-bf4d-d29c13c36c81.jpeg
tags: go, beginners, array

---

Hey folks! Today, we're diving deep into Go's built-in container types: arrays, slices, and maps. These are fundamental data structures you'll use all the time when coding in Go. Let's break them down, look at how they work, and see some extensive code examples.

# Arrays in Go

Arrays in Go are sequences of elements with a fixed size. Once you define an array, its size can't change, which can be both a limitation and an advantage depending on the use case.

## Declaring Arrays

Here are some examples of array declarations in Go:

```go
var a [3]int            // Array of 3 integers, all initialized to zero
b := [3]int{1, 2, 3}    // Array of 3 integers with specific values
c := [...]int{4, 5, 6}  // Array where size is inferred from the number of elements
```

## Copying Arrays

When you assign one array to another, Go performs a shallow copy. This means the elements are copied, not just the reference. For example:

```go
a := [3]int{1, 2, 3}
b := a                   // b is a copy of a
b[0] = 7                 // modifying b doesn't affect a
fmt.Println(a, b)        // Output: [1 2 3] [7 2 3]
```

In this example, changing `b[0]` to 7 does not affect the original array `a`, demonstrating that `b` is an independent copy of `a`.

## Fixed Size

Arrays have a fixed size, which makes them somewhat rigid. If you need a more flexible data structure, slices are the way to go.

```go
var m [4]int
var c [3]int
// m = c // This will not compile because they are different types
```

## Practical Use of Arrays

Despite their limitations, arrays can be useful in certain scenarios where a fixed size is advantageous, such as when dealing with low-level programming, implementing algorithms with a known upper limit, or working with constant data sets.

![](https://cdn.hashnode.com/res/hashnode/image/upload/v1721423221563/e6df1ef8-5e6e-4aac-91cf-47fb6befdfaa.png align="center")

```go
// Example: Implementing a simple fixed-size buffer
package main

import "fmt"

func main() {
    var buffer [10]int // fixed-size buffer of 10 elements
    for i := 0; i < 10; i++ {
        buffer[i] = i * i
    }
    fmt.Println(buffer) // Output: [0 1 4 9 16 25 36 49 64 81]
}
```

# Slices in Go

Slices are more flexible than arrays. They are dynamically-sized, allowing you to grow or shrink them as needed. Slices are essentially references to arrays with additional metadata.

![](https://cdn.hashnode.com/res/hashnode/image/upload/v1721423135297/20619b79-52e2-41a3-b721-532958e7da09.png align="center")

## Declaring Slices

Slices can be declared in various ways:

```go
var s []int              // A slice of integers
s = make([]int, 3)       // Create a slice with length 3
t := []int{1, 2, 3}      // Slice with initial values
```

## Appending to Slices

The most common function you'll see with slices is `append`. It adds elements to the end of a slice:

```go
s := []int{1, 2, 3}
s = append(s, 4, 5)      // Now s is [1, 2, 3, 4, 5]
```

If the slice doesn't have enough capacity to hold the new elements, Go allocates a new, larger array and copies the existing elements over:

```go
a := make([]int, 4, 4)   // length 4, capacity 4
a = append(a, 5)         // append element, capacity increases
fmt.Println(a)           // Output: [0 0 0 0 5]
```

In this example, the slice `a` initially has a capacity of 4. When we append the fifth element, Go allocates a new array with a larger capacity and copies the elements over.

## Slicing Slices

Slices can be created from arrays or other slices. Here's how you slice an array:

```go
arr := [5]int{1, 2, 3, 4, 5}
s := arr[1:4]            // s is [2, 3, 4]
```

And here's how you slice a slice:

```go
s := []int{1, 2, 3, 4, 5}
t := s[1:4]              // t is [2, 3, 4]
```

## Copying Slices

Slices point to an underlying array, so when you copy a slice, you're copying the reference, not the elements:

```go
a := []int{1, 2, 3}
b := a                   // b points to the same array as a
b[0] = 7
fmt.Println(a, b)        // Output: [7 2 3] [7 2 3]
```

In this example, changing `b[0]` also changes `a[0]` because `b` and `a` share the same underlying array.

## Slice Capacity and Length

Slices have both length and capacity. The length is the number of elements in the slice, while the capacity is the number of elements the slice can hold before it needs to be resized.

```go
s := []int{1, 2, 3, 4, 5}
fmt.Println(len(s))     // Output: 5
fmt.Println(cap(s))     // Output: 5

s = s[:3]
fmt.Println(len(s))     // Output: 3
fmt.Println(cap(s))     // Output: 5

s = append(s, 6)
fmt.Println(len(s))     // Output: 4
fmt.Println(cap(s))     // Output: 5
```

In this example, slicing `s` to a length of 3 does not change its capacity. Appending to `s` will use the existing capacity until it is exceeded.

## Slice Operations

Slices can be modified in various ways:

```go
a := []int{1, 2, 3, 4, 5}
a = append(a, 6)         // Appending
sub := a[1:3]            // Slicing
fmt.Println(sub)         // Output: [2 3]
```

Slices get their name because they allow you to "slice" portions of an array or another slice.

## Practical Use of Slices

Slices are widely used in Go for their flexibility. They are the go-to data structure for most everyday programming needs.

```go
// Example: Implementing a dynamic list of integers
package main

import "fmt"

func main() {
    var list []int
    for i := 0; i < 10; i++ {
        list = append(list, i*i)
    }
    fmt.Println(list) // Output: [0 1 4 9 16 25 36 49 64 81]
}
```

# Maps in Go

Maps are key-value pairs, like dictionaries in Python. They map keys to values and are very useful for various tasks.

![](https://cdn.hashnode.com/res/hashnode/image/upload/v1721423342667/87b6d3a1-0cc7-4709-ba83-45b632078711.png align="center")

## Declaring Maps

Maps are declared using the `make` function or map literals:

```go
m := make(map[string]int)  // Create an empty map
n := map[string]int{"foo": 1, "bar": 2}  // Map with initial values
```

## Adding and Retrieving Values

You can add key-value pairs to a map and retrieve them like this:

```go
m["foo"] = 1
value := m["foo"]
fmt.Println(value)         // Output: 1
```

## Checking for Key Existence

To check if a key exists in a map, you can use the following idiom:

```go
value, ok := m["foo"]
if ok {
    fmt.Println("Key exists with value", value)
} else {
    fmt.Println("Key does not exist")
}
```

## Deleting Keys

You can delete a key-value pair from a map using the `delete` function:

```go
delete(m, "foo")
```

## Map Characteristics

Maps in Go are extremely convenient. They can be read from even when empty or nil, but you can't write to a nil map. Here's an example:

```go
var m map[string]int    // m is nil
fmt.Println(m["foo"])   // Output: 0 (default value for int)
m["foo"] = 1            // Panic: assignment to entry in nil map
```

To use a map, you must initialize it:

```go
m = make(map[string]int)
m["foo"] = 1            // Now it's safe to write to m
```

## Iterating Over Maps

You can iterate over a map using a `for` loop:

```go
m := map[string]int{"foo": 1, "bar": 2}
for k, v := range m {
    fmt.Println(k, v)
}
```

## Practical Use of Maps

Maps are extremely useful for tasks like counting occurrences, indexing data, and more.

```go
// Example: Counting word occurrences in a slice of strings
package main

import "fmt"

func main() {
    words := []string{"apple", "banana", "apple", "orange", "banana", "apple"}
    wordCount := make(map[string]int)

    for _, word := range words {Go's built-in container types—arrays, slices, and maps—are powerful tools for managing collections of data. Arrays provide a fixed-size sequence of elements, slices offer dynamic resizing with more flexibility, and maps allow efficient key-value storage. Understanding these data structures and their behaviors is crucial for effective Go programming.

With arrays, you get fixed-size collections that are great for low-level tasks or constant data sets. Slices give you dynamic resizing capabilities, making them perfect for most everyday programming needs. Maps, on the other hand, provide a powerful way to store and retrieve data using key-value pairs efficiently.

By mastering these container types, you'll be well-equipped to handle a wide range of programming challenges in Go. Happy coding!
        wordCount[word]++
    }

    fmt.Println(wordCount) // Output: map[apple:3 banana:2 orange:1]
}
```

## Maps and Slices Together

Combining maps and slices can be powerful. For example, you can use a map to count occurrences and a slice to sort or store keys:

```go
package main

import (
    "fmt"
    "sort"
)

func main() {
    words := []string{"apple", "banana", "apple", "orange", "banana", "apple"}
    wordCount := make(map[string]int)

    for _, word := range words {
        wordCount[word]++
    }

    type kv struct {
        Key   string
        Value int
    }

    var ss []kv
    for k, v := range wordCount {
        ss = append(ss, kv{k, v})
    }

    sort.Slice(ss, func(i, j int) bool {
        return ss[i].Value > ss[j].Value
    })

    for _, kv := range ss {
        fmt.Printf("%s: %d\n", kv.Key, kv.Value)
    }
}
```

## Practical Example: Word Count

Let’s see a practical example where we use slices and maps to count unique words in a text and find the most common words.

### Example Code

```go
package main

import (
    "bufio"
    "fmt"
    "os"
    "sort"
    "strings"
)

func main() {
    // Initialize a map to count words
    wordCount := make(map[string]int)
    scanner := bufio.NewScanner(os.Stdin)
    scanner.Split(bufio.ScanWords)

    for scanner.Scan() {
        word := strings.ToLower(scanner.Text())
        wordCount[word]++
    }

    // Convert map to a slice of key-value pairs
    type kv struct {
        Key   string
        Value int
    }

    var ss []kv
    for k, v := range wordCount {
        ss = append(ss, kv{k, v})
    }

    // Sort slice by values in descending order
    sort.Slice(ss, func(i, j int) bool {
        return ss[i].Value > ss[j].Value
    })

    // Print the top 3 words
    for i, kv := range ss {
        if i >= 3 {
            break
        }
        fmt.Printf("%s: %d\n", kv.Key, kv.Value)
    }
}
```

### Running the Program

To run this program, provide input via standard input (stdin). Here’s how you can run it:

```bash
echo "this is a test this is only a test" | go run main.go
```

This will output the top 3 most frequent words along with their counts.

### Detailed Breakdown

Let's break down what this program does:

1. **Initialize the Map**: We create a map to store word counts.
    
2. **Scan Input**: We use a `bufio.Scanner` to read words from standard input.
    
3. **Count Words**: For each word, we convert it to lowercase and increment its count in the map.
    
4. **Convert Map to Slice**: We convert the map to a slice of key-value pairs to sort it.
    
5. **Sort the Slice**: We sort the slice by values in descending order.
    
6. **Print the Top 3 Words**: We print the top 3 most frequent words.
    

This example demonstrates how powerful and flexible Go's built-in container types can be when combined.

# Conclusion

Go's built-in container types—arrays, slices, and maps—are powerful tools for managing collections of data. Arrays provide a fixed-size sequence of elements, slices offer dynamic resizing with more flexibility, and maps allow efficient key-value storage. Understanding these data structures and their behaviors is crucial for effective Go programming.

With arrays, you get fixed-size collections that are great for low-level tasks or constant data sets. Slices give you dynamic resizing capabilities, making them perfect for most everyday programming needs. Maps, on the other hand, provide a powerful way to store and retrieve data using key-value pairs efficiently.

By mastering these container types, you'll be well-equipped to handle a wide range of programming challenges in Go. Happy coding!