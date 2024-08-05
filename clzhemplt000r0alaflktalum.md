---
title: "Unlocking Go's Power: Struct Composition and Elegant Sorting"
datePublished: Mon Aug 05 2024 19:48:47 GMT+0000 (Coordinated Universal Time)
cuid: clzhemplt000r0alaflktalum
slug: unlocking-gos-power-struct-composition-and-elegant-sorting
cover: https://cdn.hashnode.com/res/hashnode/image/upload/v1722887185359/21691e10-f2c1-4cbd-9749-c8b70a240268.png
tags: go

---

Struct composition in Go allows developers to create complex types by combining simpler ones, promoting composition over inheritance for more flexible and maintainable code. This post explores struct composition, its differences from inheritance, and provides practical examples. Additionally, we examine Go's sorting mechanism, which utilizes interfaces and methods to demonstrate the power of composition for creating flexible and reusable code.

# What is Struct Composition?

Struct composition involves embedding one struct within another without explicitly naming it as a field. This technique promotes the fields and methods of the embedded struct to the outer struct, making them accessible as if they were part of the outer struct itself.

### Basic Struct Composition

Let's start with a basic example to understand how struct composition works.

```go
package main

import (
    "fmt"
)

// Define a basic struct
type Pair struct {
    X, Y int
}

// Implement a method for Pair
func (p Pair) String() string {
    return fmt.Sprintf("Pair(%d, %d)", p.X, p.Y)
}

// Define another struct that embeds Pair
type PairWithLength struct {
    Pair
    Length int
}

func main() {
    // Create an instance of Pair
    p := Pair{X: 1, Y: 2}
    fmt.Println(p)

    // Create an instance of PairWithLength
    pl := PairWithLength{
        Pair:  Pair{X: 3, Y: 4},
        Length: 5,
    }
    fmt.Println(pl)
    fmt.Println(pl.Length)
    fmt.Println(pl.X, pl.Y) // Access fields of embedded Pair
}
```

In this example, `PairWithLength` embeds the `Pair` struct. The fields `X` and `Y` from `Pair` are promoted to `PairWithLength`, allowing direct access without additional dot notation.

### Field and Method Promotion

When a struct is embedded, its fields and methods are promoted to the embedding struct. This means you can call methods of the embedded struct directly on the outer struct.

```go
package main

import (
    "fmt"
)

// Define a method for Pair
func (p Pair) Sum() int {
    return p.X + p.Y
}

func main() {
    pl := PairWithLength{
        Pair:  Pair{X: 3, Y: 4},
        Length: 5,
    }
    
    fmt.Println(pl.Sum()) // Method of embedded Pair
}
```

Here, the `Sum` method defined for `Pair` is accessible through `PairWithLength` due to method promotion.

# Composition vs. Inheritance

A key distinction between composition and inheritance is that composition allows for more flexible code structures without creating rigid parent-child relationships. Inheritance implies a strict hierarchy, whereas composition emphasizes the assembly of complex types from simple, reusable components.

To illustrate, consider the following example demonstrating the limitations of inheritance and the flexibility of composition.

```go
package main

import (
    "fmt"
)

// Define an interface
type FileNamer interface {
    FileName() string
}

// Implement FileNamer for Pair
func (p Pair) FileName() string {
    return fmt.Sprintf("file_%d_%d", p.X, p.Y)
}

// Attempt to use PairWithLength as FileNamer
func main() {
    var fn FileNamer
    p := Pair{X: 1, Y: 2}
    fn = p
    fmt.Println(fn.FileName())

    pl := PairWithLength{
        Pair:  Pair{X: 3, Y: 4},
        Length: 5,
    }

    // This assignment works because of method promotion
    fn = pl
    fmt.Println(fn.FileName())
}
```

In this code, both `Pair` and `PairWithLength` can implement the `FileNamer` interface due to method promotion. This demonstrates how composition allows `PairWithLength` to adopt the `FileNamer` interface without inheriting from `Pair`.

### Embedding Non-Struct Types

In Go, you can also embed non-struct types, such as slices, within structs. This can be useful for creating composite types with embedded behavior.

```go
package main

import (
    "fmt"
)

// Define a type
type IntSlice []int

// Implement a method for IntSlice
func (s IntSlice) Sum() int {
    sum := 0
    for _, v := range s {
        sum += v
    }
    return sum
}

// Define a struct that embeds IntSlice
type MyStruct struct {
    IntSlice
}

func main() {
    ms := MyStruct{
        IntSlice: IntSlice{1, 2, 3, 4},
    }
    fmt.Println(ms.Sum()) // Method of embedded IntSlice
}
```

In this example, the `Sum` method of `IntSlice` is accessible through `MyStruct` due to embedding, illustrating the versatility of composition.

### Practical Example: Sorting with Composition

A practical use case for composition is implementing sorting for a custom type. Let's see how this works by embedding a slice and using Go's sort package.

```go
package main

import (
    "fmt"
    "sort"
)

// Define a type
type Person struct {
    Name string
    Age  int
}

// Define a type that embeds a slice of Person
type People struct {
    persons []Person
}

// Implement sort.Interface for People
func (p People) Len() int           { return len(p.persons) }
func (p People) Swap(i, j int)      { p.persons[i], p.persons[j] = p.persons[j], p.persons[i] }
func (p People) Less(i, j int) bool { return p.persons[i].Age < p.persons[j].Age }

func main() {
    people := People{
        persons: []Person{
            {"Alice", 30},
            {"Bob", 25},
            {"Charlie", 35},
        },
    }
    sort.Sort(people)
    fmt.Println(people)
}
```

In this example, the `People` type embeds a slice of `Person` and implements the `sort.Interface`. This allows us to sort `People` by age using Go's sort package, demonstrating the power and flexibility of struct composition.

# The Basics of Go's Sort Interface

In Go, the `sort` package provides a general-purpose interface for sorting, which requires three methods:

1. `Len() int`: Returns the length of the collection.
    
2. `Swap(i, j int)`: Swaps the elements with indexes `i` and `j`.
    
3. `Less(i, j int) bool`: Reports whether the element with index `i` should sort before the element with index `j`.
    

These methods allow Go's sort function to operate on any collection that implements this interface. Let's start with a simple example using a slice of strings.

```go
package main

import (
	"fmt"
	"sort"
)

func main() {
	strs := []string{"pear", "apple", "orange", "banana"}
	sort.Strings(strs)
	fmt.Println("Sorted strings:", strs)
}
```

In this example, `sort.Strings` sorts a slice of strings in place. Under the hood, it uses a type `sort.StringSlice`, which implements the `sort.Interface` by providing the required methods.

### Implementing Custom Sorting

Now, let's create a custom type and sort it using the `sort` package. We'll define an `Organ` type and sort a slice of `Organ` by name and weight.

```go
package main

import (
	"fmt"
	"sort"
)

// Organ represents a body organ with a name and weight.
type Organ struct {
	Name   string
	Weight int
}

// ByName implements sort.Interface based on the Name field.
type ByName []Organ

func (a ByName) Len() int           { return len(a) }
func (a ByName) Swap(i, j int)      { a[i], a[j] = a[j], a[i] }
func (a ByName) Less(i, j int) bool { return a[i].Name < a[j].Name }

// ByWeight implements sort.Interface based on the Weight field.
type ByWeight []Organ

func (a ByWeight) Len() int           { return len(a) }
func (a ByWeight) Swap(i, j int)      { a[i], a[j] = a[j], a[i] }
func (a ByWeight) Less(i, j int) bool { return a[i].Weight < a[j].Weight }

func main() {
	organs := []Organ{
		{"Heart", 300},
		{"Liver", 1500},
		{"Brain", 1400},
		{"Kidney", 150},
	}

	// Sort by name
	sort.Sort(ByName(organs))
	fmt.Println("Sorted by Name:", organs)

	// Sort by weight
	sort.Sort(ByWeight(organs))
	fmt.Println("Sorted by Weight:", organs)
}
```

# Understanding Composition in Go

Composition in Go allows us to build complex types by combining simpler ones. Unlike inheritance, composition involves embedding types within other types, promoting their methods. This approach can be more flexible and powerful.

In the example above, `ByName` and `ByWeight` both embed a slice of `Organ`. By doing so, they inherit the `Len` and `Swap` methods from the slice type, and we only need to define the `Less` method for each sorting criterion.

### Reversing Sort Order

The `sort` package also provides a way to reverse the sorting order using the `sort.Reverse` function, which wraps an existing `sort.Interface`.

```go
package main

import (
	"fmt"
	"sort"
)

func main() {
	strs := []string{"pear", "apple", "orange", "banana"}
	sort.Sort(sort.Reverse(sort.StringSlice(strs)))
	fmt.Println("Reverse sorted strings:", strs)
}
```

For our custom type, we can apply `sort.Reverse` in a similar manner.

```go
package main

import (
	"fmt"
	"sort"
)

func main() {
	organs := []Organ{
		{"Heart", 300},
		{"Liver", 1500},
		{"Brain", 1400},
		{"Kidney", 150},
	}

	// Reverse sort by weight
	sort.Sort(sort.Reverse(ByWeight(organs)))
	fmt.Println("Reverse sorted by Weight:", organs)
}
```

### Advanced Composition Example: Stack with Encapsulation

Let's explore another powerful use of composition by creating a stack data structure that encapsulates its internal workings.

```go
package main

import "fmt"

// StringStack is a stack of strings with encapsulated implementation.
type StringStack struct {
	data []string
}

// Push adds an element to the top of the stack.
func (s *StringStack) Push(str string) {
	s.data = append(s.data, str)
}

// Pop removes and returns the top element of the stack. Panics if the stack is empty.
func (s *StringStack) Pop() string {
	if len(s.data) == 0 {
		panic("pop from an empty stack")
	}
	str := s.data[len(s.data)-1]
	s.data = s.data[:len(s.data)-1]
	return str
}

func main() {
	stack := &StringStack{}
	stack.Push("apple")
	stack.Push("banana")
	fmt.Println("Popped:", stack.Pop())
	fmt.Println("Popped:", stack.Pop())
	// Uncommenting the next line will cause a panic
	// fmt.Println("Popped:", stack.Pop())
}
```

### Conclusion

Struct composition in Go offers a flexible alternative to inheritance, enhancing code maintainability and fostering better design practices. By promoting fields and methods from embedded types, developers can create complex, reusable types without rigid class hierarchies. Go's sorting mechanism, built on interfaces and methods, further illustrates the power of composition, enabling the creation of robust and maintainable applications. This post's examples highlight the elegance and efficiency of Go's design principles.