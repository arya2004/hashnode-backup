---
title: "Exploring Structs in Go and JSON Struct Tags"
datePublished: Mon Jul 29 2024 18:08:51 GMT+0000 (Coordinated Universal Time)
cuid: clz7az8kf00010al824yy1gwb
slug: structs-in-go-and-json-struct-tags
cover: https://cdn.hashnode.com/res/hashnode/image/upload/v1722274894121/66ebdd89-76c6-49da-81df-ca683d27a45c.png
tags: go, json, struct

---

# Introduction

In this technical deep dive, we'll explore the concept of `structs` in Go, delve into how Go handles JSON, and examine the powerful feature of `struct tags`. Structs in Go are pivotal for creating complex data types, and struct tags play an essential role in controlling how Go's JSON package handles JSON encoding and decoding. We'll cover the following key points:

1. What are structs in Go?
    
2. Creating and manipulating structs.
    
3. Using pointers with structs.
    
4. JSON encoding and decoding with struct tags.
    

# Understanding Structs

A `struct` in Go is a composite data type that groups together variables under a single name. These variables, known as fields, can be of different types.

### Basic Struct Example

Here's a basic example to demonstrate the creation and initialization of a struct:

```go
package main

import (
	"fmt"
)

type Employee struct {
	Name   string
	Number int
	Hired  string
	Boss   *Employee
}

func main() {
	// Creating an empty Employee struct
	var e Employee
	fmt.Printf("%+v\n", e)

	// Initializing fields using dot notation
	e.Name = "Matt"
	e.Number = 1
	e.Hired = "2024-07-29"
	fmt.Printf("%+v\n", e)

	// Creating a struct literal
	e2 := Employee{
		Name:   "Lamine",
		Number: 2,
		Hired:  "2023-05-16",
		Boss:   &e,
	}
	fmt.Printf("%+v\n", e2)
}
```

![](https://cdn.hashnode.com/res/hashnode/image/upload/v1722276416114/b8a9e69c-c185-4624-b553-e730c4e5abd7.png align="center")

## Pointers and Nested Structs

Using pointers in structs is crucial for creating hierarchical relationships, such as an employee having a boss, where the boss is also an employee.

![](https://cdn.hashnode.com/res/hashnode/image/upload/v1722276388688/88bf4c3e-37f3-4cba-84fa-abd2941d4935.png align="center")

#### Example with Pointers

```go
package main

import (
	"fmt"
)

type Employee struct {
	Name   string
	Number int
	Hired  string
	Boss   *Employee
}

func main() {
	// Creating Employee structs
	boss := &Employee{
		Name:   "Alice",
		Number: 1,
		Hired:  "2020-01-01",
	}

	employee := &Employee{
		Name:   "Bob",
		Number: 2,
		Hired:  "2021-02-02",
		Boss:   boss,
	}

	// Displaying employees
	fmt.Printf("%+v\n", *boss)
	fmt.Printf("%+v\n", *employee)
}
```

## What Are Struct Tags?

Struct tags are strings that provide metadata for struct fields. They are enclosed in backticks and follow a specific format. Here's a simple example:

```go
type Response struct {
    Page  int    `json:"page"`
    Words string `json:"words,omitempty"`
}
```

In this example, the struct `Response` has two fields: `Page` and `Words`. The struct tags `json:"page"` and `json:"words,omitempty"` provide information on how these fields should be handled when converting to and from JSON.

## Struct Tag Format

The format of a struct tag is typically:

```go
`key:"value"`
```

You can have multiple key-value pairs separated by spaces. For example:

```go
`json:"page,omitempty" xml:"page"`
```

Go doesn't prescribe what the keywords are, but certain libraries, such as the encoding/json package, understand specific keywords like `json`.

# JSON Encoding with Struct Tags

Struct tags are commonly used for JSON encoding and decoding. Let's see how it works with an example.

### Example: Encoding a Struct to JSON

Here's a Go program that demonstrates encoding a struct to JSON:

```go
package main

import (
    "encoding/json"
    "fmt"
)

type Response struct {
    Page  int    `json:"page"`
    Words string `json:"words,omitempty"`
}

func main() {
    r := Response{
        Page:  1,
        Words: "Hello, World!",
    }

    jsonData, err := json.Marshal(r)
    if err != nil {
        fmt.Println("Error encoding JSON:", err)
        return
    }

    fmt.Println(string(jsonData))
}
```

Output:

```go
{"page":1,"words":"Hello, World!"}
```

In this example, the `json:"page"` tag tells the JSON encoder to use "page" as the JSON key for the `Page` field. The `json:"words,omitempty"` tag tells the encoder to use "words" as the key for the `Words` field and to omit it if the field is empty.

### Example: Decoding JSON to a Struct

Let's decode a JSON string back into a struct:

```go
package main

import (
    "encoding/json"
    "fmt"
)

type Response struct {
    Page  int    `json:"page"`
    Words string `json:"words,omitempty"`
}

func main() {
    jsonData := `{"page":1,"words":"Hello, World!"}`
    var r Response

    err := json.Unmarshal([]byte(jsonData), &r)
    if err != nil {
        fmt.Println("Error decoding JSON:", err)
        return
    }

    fmt.Printf("%+v\n", r)
}
```

Output:

```json
{Page:1 Words:Hello, World!}
```

In this example, `json.Unmarshal` reads the JSON string and populates the fields of the `Response` struct based on the struct tags.

## Omitting Empty Fields

The `omitempty` option in struct tags is useful when you don't want to include fields with zero values in the JSON output. Let's see how it works:

```go
package main

import (
    "encoding/json"
    "fmt"
)

type Response struct {
    Page  int    `json:"page"`
    Words string `json:"words,omitempty"`
}

func main() {
    r := Response{
        Page: 1,
    }

    jsonData, err := json.Marshal(r)
    if err != nil {
        fmt.Println("Error encoding JSON:", err)
        return
    }

    fmt.Println(string(jsonData))
}
```

Output:

```json
{"page":1}
```

Here, since the `Words` field is empty, it is omitted from the JSON output.

## Exported and Unexported Fields

In Go, only exported fields (those starting with an uppercase letter) can be encoded to JSON. Let's see what happens if we have an unexported field:

```go
package main

import (
    "encoding/json"
    "fmt"
)

type Response struct {
    page  int    `json:"page"`
    Words string `json:"words,omitempty"`
}

func main() {
    r := Response{
        page:  1,
        Words: "Hello, World!",
    }

    jsonData, err := json.Marshal(r)
    if err != nil {
        fmt.Println("Error encoding JSON:", err)
        return
    }

    fmt.Println(string(jsonData))
}
```

Output:

```json
{"words":"Hello, World!"}
```

Since `page` is unexported (starts with a lowercase letter), it is not included in the JSON output. Additionally, the Go vet tool will warn you if you have a struct tag for an unexported field, as it's likely a mistake.

# Using Struct Tags for Databases

Struct tags can also be used for database operations. Here's an example with the `gorm` ORM:

```go
package main

import (
    "fmt"
    "gorm.io/driver/sqlite"
    "gorm.io/gorm"
)

type User struct {
    ID   uint   `gorm:"primaryKey"`
    Name string `gorm:"column:username"`
}

func main() {
    db, err := gorm.Open(sqlite.Open("test.db"), &gorm.Config{})
    if err != nil {
        fmt.Println("Error connecting to database:", err)
        return
    }

    db.AutoMigrate(&User{})

    user := User{Name: "John Doe"}
    db.Create(&user)

    var retrievedUser User
    db.First(&retrievedUser, user.ID)

    fmt.Printf("%+v\n", retrievedUser)
}
```

In this example, the struct tags provide metadata for GORM, an ORM for Go. The `gorm:"primaryKey"` tag marks the `ID` field as the primary key, and the `gorm:"column:username"` tag specifies the column name in the database.

![](https://cdn.hashnode.com/res/hashnode/image/upload/v1722276431900/de7e594d-2954-47da-94bf-6aa357a440ba.png align="center")

# Conclusion

Structs in Go are powerful tools for creating complex data types, and understanding how to manipulate them is crucial for effective Go programming. This exploration of structs in Go provides a foundation for building robust and maintainable applications.

Struct tags in Go are a powerful feature that allow you to add metadata to struct fields. This metadata can control how the struct's data is encoded and decoded, whether for JSON, XML, or databases. By understanding and using struct tags effectively, you can make your Go programs more robust and easier to maintain.