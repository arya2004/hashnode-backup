---
title: "The Definitive Guide to Golang Design Patterns"
seoTitle: "The Definitive Guide to Golang Design Patterns"
seoDescription: "From Factory Method to Visitor: Practical Patterns for Better Go Code"
datePublished: Tue Jul 01 2025 13:57:28 GMT+0000 (Coordinated Universal Time)
cuid: cmckle1ko000202l7el7i3cxh
slug: the-definitive-guide-to-golang-design-patterns
cover: https://cdn.hashnode.com/res/hashnode/image/upload/v1751375432538/65d82d8e-2612-49fb-97de-61617f4aa6e6.png
tags: design-patterns, go, design-principles

---

In the world of software engineering, design patterns are like ready-made solutions for common problems we face in coding. If you are a Go developer, you may have seen situations where your code starts to get tangled, difficult to test, or hard to maintain. Design patterns help us write code that is cleaner, more flexible, and easier to extend.

This blog is your one-stop guide to the most useful design patterns in Go. We’ll start from the basics, creational patterns for object creation, move on to structural patterns for organising code, and finally cover behavioural patterns for smarter program flow. For each pattern, you’ll see real-world code examples, understand common problems, and learn simple, idiomatic solutions using Go’s unique strengths. We’ll also show you how to make your code goroutine-safe wherever it matters.

Whether you are a beginner or an experienced developer looking to refresh your knowledge, this guide is made for you. Let’s make Go coding smarter and more enjoyable one pattern at a time.

---

# Creational Design Patterns

Creational design patterns help manage and simplify the process of object creation. They abstract the instantiation mechanism, ensuring that your Go applications remain flexible and reusable. By using these patterns, you avoid unnecessary complexity, reduce direct dependency on specific implementations, and make it easier to manage object lifecycles effectively.

The Creational patterns you'll explore in this section include methods to create objects, reuse existing instances, and abstract complex construction logic.

## Factory Method

> **Factory Method** is a creational design pattern that provides an interface for creating objects in a superclass, but allows subclasses to alter the type of objects that will be created.

Imagine you're building a simple application that saves files to disk. You might directly use a struct `Storage` for this purpose, which handles saving and loading files directly.

```go
package main

import (
	"fmt"
	"os"
)

type Storage struct {
	basePath string		
}

func NewStorage(basePath string) *Storage {
	return &Storage{
		basePath: basePath,	
	}
}

func (s *Storage) Save(name string, data []byte) error {
	fullPath := s.basePath + "/" + name
	return os.WriteFile(fullPath, data, 0666)
}

func (s *Storage) Load(name string) ([]byte, error) {
	fullPath := s.basePath + "/" + name
	return os.ReadFile(fullPath)
}


func main() {
	storage := NewStorage("./")
	err := storage.Save("record.txt", []byte("hello world"))	

	if err != nil {
		panic(err)	
	}

	data, err := storage.Load("record.txt")	

	if err != nil {
		panic(err)
	}


	fmt.Println("data: ", string(data))
}
```

### Problems With That Code

* **Tight Coupling**: Your main application directly depends on file system operations. Changing storage type (e.g., to memory, database, or cloud) will be very difficult.
    
* **Less Testable**: Unit testing is difficult because you cannot easily replace file-system storage with mock or memory storage.
    
* **Difficult to Extend**: Adding more storage types means directly modifying existing code.
    

The **Factory Method Pattern** introduces an interface that defines the object creation method. Instead of instantiating concrete objects directly, you create them through a factory method, allowing flexibility.

In simple terms, instead of directly creating `LocalStorage`, you ask the factory to give you storage, and it decides which one to create.

This solves our problems by:

* Decoupling storage creation from usage.
    
* Allowing easy addition of new storage types.
    
* Simplifying testing and extensibility.
    

Refer to the diagram:

![](https://cdn.hashnode.com/res/hashnode/image/upload/v1751369298279/1ed69d82-fa37-494a-ae53-6275a6a30ac6.png align="center")

### Code Using the Factory Method Pattern

Here’s how you'd structure your code with the Factory Method Pattern.  

```go
package main

import (
	"errors"
	"fmt"
	"os"
)

//parent interface
type Storage interface {
	Save(name string, data []byte) error
	Load(name string) ([]byte, error)
}



//implementation
type LocalStorage struct {
	basePath string	
}

func NewLocalStorage(bp string) *LocalStorage {
	return &LocalStorage{
		basePath: bp,
	}
}


func (ls *LocalStorage) Save(name string, data []byte) error {
	fullPath := ls.basePath + "/" + name
	return os.WriteFile(fullPath, data, 0644)
}

func (ls *LocalStorage) Load(name string) ([]byte, error) {
	fullPath := ls.basePath + "/" + name
	return os.ReadFile(fullPath)
}


//implementation


type MemoryStorage struct {
	files map[string][]byte
}

func NewMemoryStorage() *MemoryStorage {
	return &MemoryStorage{
		files: make(map[string][]byte),
	}
}

func (ms *MemoryStorage) Save(name string, data []byte) error {
	ms.files[name] = append([]byte(nil), data...)
	return nil
}

func (ms *MemoryStorage) Load(name string) ([]byte, error) {
	data, ok := ms.files[name]
	if !ok {
		return nil , errors.New("not found")
	}

	return append([]byte(nil), data...), nil
}

//factory

func NewStorageDriver(driver string, basePath string) ( Storage, error) {

	switch driver {
	case "local":
		return NewLocalStorage(basePath), nil

	case "memory":
		return NewMemoryStorage(), nil
	default:
		return nil, errors.New("unknown driver")
	}


}


func main() {
	localStore, err := NewStorageDriver("local", "./")
	if err != nil {
		panic(err)
	}

	localStore.Save("file1.txt", []byte("persisted to disk"))
	loadedData, err := localStore.Load("file1.txt")

	if err != nil {
		panic(err)
	}
	
	fmt.Println("localStore data: ", string(loadedData))

	memStore, err := NewStorageDriver("memory", "")
	if err != nil {
		panic(err)
	}

	memStore.Save("file2.txt", []byte("stored in memory"))
	loadedFromMemData, err := memStore.Load("file2.txt")

	if err != nil {
		panic(err)
	}

	fmt.Println("memory storage:", string(loadedFromMemData))

}
```

### Goroutine-Safe Version

In cases where your storage solution might be accessed concurrently (multiple goroutines at the same time), you must ensure thread safety.

For instance, `MemoryStorage` could cause data races without proper synchronization. A simple and effective way to ensure thread-safety is by using `sync.RWMutex`.  

```go
package main

import (
	"errors"
	"fmt"
	"os"
	"sync"
)

//parent interface
type Storage interface {
	Save(name string, data []byte) error
	Load(name string) ([]byte, error)
}



//already thread safe
type LocalStorage struct {
	basePath string	
}

func NewLocalStorage(bp string) *LocalStorage {
	return &LocalStorage{
		basePath: bp,
	}
}


func (ls *LocalStorage) Save(name string, data []byte) error {
	fullPath := ls.basePath + "/" + name
	return os.WriteFile(fullPath, data, 0644)
}

func (ls *LocalStorage) Load(name string) ([]byte, error) {
	fullPath := ls.basePath + "/" + name
	return os.ReadFile(fullPath)
}


//implementation


type MemoryStorage struct {
	mu sync.RWMutex
	files map[string][]byte
}

func NewMemoryStorage() *MemoryStorage {
	return &MemoryStorage{
		files: make(map[string][]byte),
	}
}

func (ms *MemoryStorage) Save(name string, data []byte) error {
	
	ms.mu.Lock()
	defer ms.mu.Unlock()
	ms.files[name] = append([]byte(nil), data...)
	return nil
}

func (ms *MemoryStorage) Load(name string) ([]byte, error) {
	
	ms.mu.RLock()
	defer ms.mu.RUnlock()
	data, ok := ms.files[name]
	if !ok {
		return nil , errors.New("not found")
	}

	return append([]byte(nil), data...), nil
}

//factory

func NewStorageDriver(driver string, basePath string) ( Storage, error) {

	switch driver {
	case "local":
		return NewLocalStorage(basePath), nil

	case "memory":
		return NewMemoryStorage(), nil
	default:
		return nil, errors.New("unknown driver")
	}


}


func main() {
	localStore, err := NewStorageDriver("local", "./")
	if err != nil {
		panic(err)
	}

	localStore.Save("file1.txt", []byte("persisted to disk"))
	loadedData, err := localStore.Load("file1.txt")

	if err != nil {
		panic(err)
	}
	
	fmt.Println("localStore data: ", string(loadedData))

	memStore, err := NewStorageDriver("memory", "")
	if err != nil {
		panic(err)
	}

	memStore.Save("file2.txt", []byte("stored in memory"))
	loadedFromMemData, err := memStore.Load("file2.txt")

	if err != nil {
		panic(err)
	}

	fmt.Println("memory storage:", string(loadedFromMemData))

	//concurrency

	var wg sync.WaitGroup
	mem, err := NewStorageDriver("memory", "")
	if err != nil {
		panic(err)
	}

	for i := 0; i < 10; i++ {
		wg.Add(1)
		go func(idx int) {
			defer wg.Done()
			fileName := "concurrent.txt"
			mem.Save(fileName, []byte("data from goroutine"))
			data, err := mem.Load(fileName)
			if err != nil {
				panic(err)
			}
			fmt.Println("data from ", idx, "is: ", string(data))
		}(i)
	}

	wg.Wait()

}
```

The Factory Method Pattern is beneficial in Go for several reasons:

* **Extensible**: You can add new storage types easily without changing existing client code.
    
* **Decoupling**: Client code depends on interfaces rather than concrete implementations.
    
* **Testable**: Easy to mock storage for unit tests.
    

This pattern aligns nicely with Go’s idiomatic practices of using interfaces for better abstraction and maintainability.

## Builder

> **Builder** is a creational design pattern that lets you construct complex objects step by step. The pattern allows you to produce different types and representations of an object using the same construction code.

Consider you're developing a configuration loader for your application. You directly load configuration from the environment and JSON files, handling each separately.  

```go
package main

import (
	"encoding/json"
	"errors"
	"fmt"
	"os"
)


type Config struct {
	Host string
	Port string 
	EnableTLS bool
}

func LoadConfigFronEnv() (*Config, error) {
	cfg := &Config{}
	cfg.Host = os.Getenv("HOST")	

	port := os.Getenv("PORT")
	if port == "" {
		return nil, errors.New("env var PORT not set")
	}

	cfg.Port = port

	cfg.EnableTLS = os.Getenv("TLS") == "1"
	return cfg, nil

}


func LoadConfigFromJSON(file string) (*Config, error) {
	f, err := os.Open(file)
	if err != nil {
		return nil, err
	}

	defer f.Close()

	dec := json.NewDecoder(f)
	var cfg Config
	if err := dec.Decode(&cfg); err != nil {
		return nil, err
	}

	return &cfg, nil
}



func main() {

	os.Setenv("HOST", "google.com")
	os.Setenv("PORT", "8888")
	os.Setenv("EnableTLS", "1")

	envConfig, err := LoadConfigFronEnv()
	if err != nil {
		panic(err)
	}

	fmt.Println("env: ", envConfig)

	jsonConfig, err := LoadConfigFromJSON("config.json")	
	if err != nil {
		panic(err)
	}

	fmt.Println("json: ", jsonConfig)

}
```

### Problems With That Code

* **Complex Initialization**: Managing object creation from multiple sources is tedious.
    
* **Hard to Maintain**: Any new source or rule means modifying existing code significantly.
    
* **Difficult to Extend**: Adding additional configuration sources becomes cumbersome.
    
* **Lack of Clarity**: Client code becomes messy with multiple if-else blocks for loading configurations.
    

The **Builder Pattern** introduces a separate `Builder` interface that encapsulates object construction. Instead of directly constructing complex objects, the client uses a builder step-by-step to set up the configuration, simplifying the complexity.

The pattern involves:

* A **Director** that manages the build process (optional in simple Go scenarios).
    
* A **Builder Interface** defining individual build steps.
    
* **Concrete Builders** that provide specific implementations for constructing the object.
    

This solves earlier problems by:

* **Simplifying object construction** by chaining methods clearly.
    
* **Enhancing flexibility and readability**, clearly separating construction logic from business logic.
    
* **Easily extendable** to add more sources without changing client logic.
    

Refer to the diagram:

![](https://cdn.hashnode.com/res/hashnode/image/upload/v1751369802983/2e667729-7258-4396-b6a0-77d05caaf7bf.png align="center")

* `Client` initiates the build via a `Director` (or directly).
    
* `Director` manages and orchestrates the construction sequence.
    
* `ConcreteBuilders` handle specific implementations.
    
* Final objects (`Product1`, `Product2`) constructed step-by-step.
    

### Code Using the Builder Pattern

Implement the Builder Pattern clearly defining a builder interface and concrete implementations to simplify configuration loading.  

```go
package main

import (
	"encoding/json"
	"errors"
	"fmt"
	"os"
)

type Config struct {
	Host      string
	Port      string
	EnableTLS bool
}

type ConfigBuilder interface {
	FromEnv() ConfigBuilder
	FromJson(file string) ConfigBuilder
	WithoutDefaultHost(host string) ConfigBuilder
	Build() (*Config, error)
}

type builder struct {
	cfg Config
	err error
}



func NewConfigBuilder() ConfigBuilder {
	return &builder{}
}


// Build implements ConfigBuilder.
func (b *builder) Build() (*Config, error) {
	if b.err != nil {
		return nil, b.err
	}

	if b.cfg.Host == "" {
		return nil, errors.New("host required")	
	}
	if b.cfg.Port == "" {
		b.cfg.Port = "8080"
	}
	return &b.cfg, nil
}

// FromEnv implements ConfigBuilder.
func (b *builder) FromEnv() ConfigBuilder {
	
	if b.err != nil {
		return b
	}

	host := os.Getenv("HOST")
	if host != "" {
		b.cfg.Host = host
	}

	port := os.Getenv("PORT")
	if port != "" {
		b.cfg.Port = port
	}

	b.cfg.EnableTLS = os.Getenv("TLS") == "1"

	return b


}

// FromJson implements ConfigBuilder.
func (b *builder) FromJson(file string) ConfigBuilder {
	
	if b.err != nil {
		return b
	}

	f, err := os.Open(file)
	if err != nil {
		b.err = err
		return b
	}

	defer f.Close()

	def := json.NewDecoder(f)
	var tmp Config
	if err := def.Decode(&tmp); err != nil {
		b.err = err
		return b
	}

	if b.cfg.Host == "" {
		b.cfg.Host = tmp.Host
	}
	if b.cfg.Port == "" {
		b.cfg.Port = tmp.Port
	}

	if !b.cfg.EnableTLS {
		b.cfg.EnableTLS = tmp.EnableTLS
	}

	return b

}

// WithoutDefaultHost implements ConfigBuilder.
func (b *builder) WithoutDefaultHost(host string) ConfigBuilder {
	if b.err != nil {
		return b
	}
	if b.cfg.Host == "" {
		b.cfg.Host = host
	}

	return b
}


func main() {

	os.Setenv("HOST", "google.com")
	os.Setenv("EnableTLS", "0")


	cfg, err := NewConfigBuilder().FromEnv().FromJson("config.json").WithoutDefaultHost("localhost").Build()

	if err != nil {
		panic(err)
	}

	fmt.Println("config: ", cfg)

}
```

### Goroutine-Safe Version

In concurrent scenarios, builders may be accessed simultaneously by multiple goroutines. Ensuring thread-safety using synchronization mechanisms like `sync.Mutex` helps to prevent race conditions and data inconsistencies.  

```go
package main

import (
	"encoding/json"
	"errors"
	"fmt"
	"os"
	"sync"
)

type Config struct {
	Host      string
	Port      string
	EnableTLS bool
}

type ConfigBuilder interface {
	FromEnv() ConfigBuilder
	FromJson(file string) ConfigBuilder
	WithoutDefaultHost(host string) ConfigBuilder
	Build() (*Config, error)
}

type builder struct {
	mu sync.Mutex
	cfg Config
	err error
}



func NewConfigBuilder() ConfigBuilder {
	return &builder{}
}


// Build implements ConfigBuilder.
func (b *builder) Build() (*Config, error) {

	b.mu.Lock()
	defer b.mu.Unlock()

	if b.err != nil {
		return nil, b.err
	}

	if b.cfg.Host == "" {
		return nil, errors.New("host required")	
	}
	if b.cfg.Port == "" {
		b.cfg.Port = "8080"
	}
	return &b.cfg, nil
}

// FromEnv implements ConfigBuilder.
func (b *builder) FromEnv() ConfigBuilder {

	b.mu.Lock()
	defer b.mu.Unlock()
	
	if b.err != nil {
		return b
	}

	host := os.Getenv("HOST")
	if host != "" {
		b.cfg.Host = host
	}

	port := os.Getenv("PORT")
	if port != "" {
		b.cfg.Port = port
	}

	b.cfg.EnableTLS = os.Getenv("TLS") == "1"

	return b


}

// FromJson implements ConfigBuilder.
func (b *builder) FromJson(file string) ConfigBuilder {
	
	b.mu.Lock()
	defer b.mu.Unlock()

	if b.err != nil {
		return b
	}

	f, err := os.Open(file)
	if err != nil {
		b.err = err
		return b
	}

	defer f.Close()

	def := json.NewDecoder(f)
	var tmp Config
	if err := def.Decode(&tmp); err != nil {
		b.err = err
		return b
	}

	if b.cfg.Host == "" {
		b.cfg.Host = tmp.Host
	}
	if b.cfg.Port == "" {
		b.cfg.Port = tmp.Port
	}

	if !b.cfg.EnableTLS {
		b.cfg.EnableTLS = tmp.EnableTLS
	}

	return b

}

// WithoutDefaultHost implements ConfigBuilder.
func (b *builder) WithoutDefaultHost(host string) ConfigBuilder {
	
	b.mu.Lock()
	defer b.mu.Unlock()
	
	if b.err != nil {
		return b
	}
	if b.cfg.Host == "" {
		b.cfg.Host = host
	}

	return b
}


func main() {

	os.Setenv("HOST", "google.com")
	os.Setenv("EnableTLS", "0")

	cfgChan := make(chan *Config)
	errChan := make(chan error)

	builder := NewConfigBuilder()


	for i := 0; i < 10; i++ {
		go func(idx int) {
		fmt.Println("called goroutine: ", idx)
		cfg, err := builder.FromEnv().FromJson("config.json").WithoutDefaultHost("localhost").Build()
		if err != nil {
			errChan <- err
			return	
		}

		cfgChan <- cfg
		}(i)
	}

	

	select {
	case cfg := <-cfgChan:
		fmt.Println("config: ", cfg)
	case err := <-errChan:
		panic(err)
	}


	


}
```

The Builder pattern provides several advantages for Go developers:

* **Clearer API**: Step-by-step construction is intuitive and easy to read.
    
* **Extensibility**: Easy to add new ways of building configurations without breaking existing code.
    
* **Isolation of complexity**: Keeps object construction logic separate from object usage logic.
    

This pattern promotes cleaner, idiomatic, and maintainable Go code by clearly defining responsibilities and improving readability, especially in large-scale applications.. However, Builder can be overkill if your object creation is simple or involves only one data source. It is ideal when constructing complex objects from multiple sources or configurations.

## Singleton

> Singleton is a creational design pattern that lets you ensure that a class has only one instance, while providing a global access point to this instance.

Let’s start with a common scenario: loading an application configuration only once and then accessing it from anywhere in your Go program.  

```go
package main

import (
	"errors"
	"fmt"
	"os"
)

type Config struct {
	data map[string]string
}

//global native
var config *Config

func LoadConfig(path string) error {
	if config != nil {
		return errors.New("config already loaded")
	}
	bytes, err := os.ReadFile(path)
	if err != nil {
		return err
	}

	//config in form key=value
	data := make(map[string]string)
	lines := bytes
	start := 0

	for i, b := range lines {
		
		if b == '\n' || i == len(lines) - 1 {
			line := lines[start:i]
			if i == len(lines) - 1 && b != '\n' {
				line = lines[start: i + 1]
			}
			sep  := -1
			for j, c := range line {
				if c == '=' {
					sep = j
					break
				}
			}

			if sep != -1 {
				k := string(line[:sep])
				v := string(line[sep+ 1:])
				data[k] = v
			}

			start = i + 1
		}


	}

	config = &Config{data: data}

	return nil

}

func GetConfigValue(key string) (string, bool) {
	if config == nil {
		return "", false
	}

	val, ok := config.data[key]
	return  val, ok
}


func main() {
	if err := LoadConfig("config.txt"); err != nil {
		panic(err)
	}

	if val, ok := GetConfigValue("PORT"); ok {
		fmt.Println("value for PORT: ", val)
	}
}
```

### Problems With That Code

* **Global state management:** Using a global variable is error-prone and hard to test or mock.
    
* **No protection against multiple initialization:** If two goroutines call the loader at the same time, you might get two instances.
    
* **Difficult to enforce one instance:** You need manual checks everywhere you access or create the config.
    
* **Concurrency issues:** Not thread-safe, which is risky in concurrent Go applications.
    

The **Singleton pattern** wraps instance creation logic, ensuring only one object exists throughout the application.  
It provides a global access point and handles concurrency using sync primitives.

![](https://cdn.hashnode.com/res/hashnode/image/upload/v1751378034273/e3a7e690-4e8c-44f6-a303-6a8c792551fb.png align="center")

As per the diagram:

* `Singleton` has a private static instance variable.
    
* Only the `getInstance()` method can initialize or return the single instance.
    
* Proper locking is required in multi-threaded apps to avoid double initialization.
    

In Go, the idiomatic way to implement Singleton is with `sync.Once`.  
This guarantees that the initialization code runs only once, even with multiple goroutines.

### Code Using the Design Pattern

Define your struct (`Config`), and use `sync.Once` to ensure initialization only happens once, even with concurrent access.  

```go
package main

import (
	"errors"
	"fmt"
	"os"
	"sync"
)

type Config struct {
	data map[string]string
}

var instance *Config
var once sync.Once

func NewConfigFromFile(path string) (*Config, error) {

	bytes, err := os.ReadFile(path)

	if err != nil {
		return nil, err
	}

	data := make(map[string]string)
	lines := bytes
	start := 0

	for i, b := range lines {
		
		if b == '\n' || i == len(lines) - 1 {
			line := lines[start:i]
			if i == len(lines) - 1 && b != '\n' {
				line = lines[start:i + 1]
			}

			sep := -1
			for j, c := range line {
				if c == '=' {
					sep = j
					break
				}
			}

			if sep != -1 {
				k := string(line[:sep])
				v := string(line[sep + 1:])
				data[k] = v
			}

			start = i + 1
		}

	}

	return &Config{
		data: data,
	}, nil;
}


func GetConfig(path string) (*Config, error) {
	var err error

	once.Do(func() {
		instance, err = NewConfigFromFile(path)
	})

	if instance == nil && err == nil {
		return nil, errors.New("config not initialized")
	}

	return instance, err
}


func (c *Config) Value(key string) (string, bool) {
	val, ok := c.data[key]
	return val, ok
	
}


func main() {
	config, err := GetConfig("config.txt")	
	if err != nil {
		panic(err)
	}

	if val, ok := config.Value("PORT"); ok {
		fmt.Println("value for PORT: ", val)
	}
}
```

### Goroutine-Safe Version

In the goroutine-safe version, the use of `sync.Once` ensures thread safety.  
Even if 10 goroutines call `GetConfig()` at the same time, only one will initialize the config, and all will get the same pointer.  

```go
package main

import (
	"errors"
	"fmt"
	"os"
	"sync"
)

type Config struct {
	data map[string]string
}

var instance *Config
var once sync.Once

func NewConfigFromFile(path string) (*Config, error) {

	bytes, err := os.ReadFile(path)

	if err != nil {
		return nil, err
	}

	data := make(map[string]string)
	lines := bytes
	start := 0

	for i, b := range lines {
		
		if b == '\n' || i == len(lines) - 1 {
			line := lines[start:i]
			if i == len(lines) - 1 && b != '\n' {
				line = lines[start:i + 1]
			}

			sep := -1
			for j, c := range line {
				if c == '=' {
					sep = j
					break
				}
			}

			if sep != -1 {
				k := string(line[:sep])
				v := string(line[sep + 1:])
				data[k] = v
			}

			start = i + 1
		}

	}

	return &Config{
		data: data,
	}, nil;
}


func GetConfig(path string) (*Config, error) {
	var err error

	once.Do(func() {
		instance, err = NewConfigFromFile(path)
	})

	if instance == nil && err == nil {
		return nil, errors.New("config not initialized")
	}

	return instance, err
}


func (c *Config) Value(key string) (string, bool) {
	val, ok := c.data[key]
	return val, ok
	
}


func main() {


	var wg sync.WaitGroup
	for i := 0; i < 10; i++ {
		wg.Add(1)
		go func(idx int) {
			defer wg.Done()
			config, err := GetConfig("config.txt")	
			if err != nil {
				panic(err)
			}
			if val, ok := config.Value("PORT"); ok {
			fmt.Println("value for PORT: ", val, "from: ", idx)
	}
		}(i)
	}

	wg.Wait()

	

	
}
```

The Singleton pattern in Go is:

* **Safe for concurrency:** Idiomatic Go uses `sync.Once` for thread safety.
    
* **Simple global access:** You get a global, single instance.
    
* **Testable:** Easier to manage test setup/reset by wrapping instance logic.
    
* **Minimal boilerplate:** Go’s `sync.Once` makes the pattern clean and robust.
    

Singleton can make unit testing harder if overused, so use it mainly for things like configuration, logging, or similar resources that should only exist once in the app. For most configuration, connection pools, or logging services, Singleton fits perfectly, as shown above. For general data, prefer dependency injection or factory patterns.

---

# Structural Design Patterns

Structural design patterns focus on the composition of objects and their interactions. They guide you on how classes and objects can be organized and combined to form larger, more flexible, and easily maintainable structures. In Go, structural patterns simplify managing dependencies, connecting components seamlessly, and adapting existing code to new requirements without extensive refactoring.

This section covers patterns that enhance flexibility, readability, and maintainability by clearly defining relationships among objects.

## Adapter

> **Adapter** is a structural design pattern that allows objects with incompatible interfaces to collaborate.

Consider you're implementing logging for your application directly using file-based logging, which writes logs directly to a file without any abstraction.  

```go
package main

import (
	"log"
	"os"
)

type MyLogger struct {
	file *os.File
}

func NewMyLogger(path string) (*MyLogger, error) {
	f, err := os.OpenFile(path, os.O_CREATE|os.O_APPEND|os.O_WRONLY, 0644)
	if err != nil {
		return nil, err
	}

	return &MyLogger{file: f}, err
}

func (l *MyLogger) Info(msg string) error {
	_, err := l.file.WriteString("[INFO] " + msg + "\n")
	return err
}

func (l *MyLogger) Error(msg string) error {
	_, err := l.file.WriteString("[ERROR] " + msg + "\n")
	return err
}

func main() {

	logger, err := NewMyLogger("app.log")
	if err != nil {
		log.Fatalf("failed to create logger: %v", err)
	}
	_ = logger.Info("service started")
	_ = logger.Error("null pointer exception")

}
```

### Problems With That Code

* **Tight coupling**: Your application code directly depends on a specific logging implementation (`MyLogger`).
    
* **Difficult to change**: If you want to switch to another logging library or standard logger, you must rewrite your entire logging logic.
    
* **Limited Flexibility**: Not easy to swap or combine different logging implementations.
    

The **Adapter pattern** helps solve compatibility issues by wrapping an incompatible object in an adapter class that translates requests between client and wrapped object.

In this case, imagine your `Client` expects a specific logging interface (`Logger`). You already have logging solutions (`FileLogger`, `StdLogger`) that don’t exactly fit the interface expected by the client.

Here, you create an **Adapter** (`StdLoggerAdapter`) to translate the method calls into compatible format.

* Client interacts only with the `Logger` interface.
    
* Adapter translates the calls to a different underlying implementation.
    

![](https://cdn.hashnode.com/res/hashnode/image/upload/v1751375039331/040a8360-963b-4ef5-a403-f9c223e18271.png align="center")

* `Client` calls methods defined by `Client Interface`.
    
* The Adapter implements the client interface, holding a reference (`adaptee`) to an incompatible service.
    
* Adapter translates calls to `serviceMethod` calls of the incompatible service.
    

### Code Using the Adapter Pattern

Implementing an Adapter Pattern allows you to integrate multiple logging implementations smoothly under a common interface, enhancing flexibility and reducing coupling.  

```go
package main

import (
	"log"
	"os"
)

type Logger interface {
	Info(msg string) error
	Error(msg string) error
}

type FileLogger struct {
	file *os.File
}


func NewFileLogger(path string) (*FileLogger, error) {
	f, err := os.OpenFile(path, os.O_CREATE|os.O_APPEND|os.O_WRONLY, 0644)
	if err != nil {
		return nil, err 
	}

	return &FileLogger{file: f}, nil
}


func (l *FileLogger) Info(msg string) error {
	_, err := l.file.WriteString("[INFO] " + msg + "\n")
	return err
}
func (l *FileLogger) Error(msg string) error {
	_, err := l.file.WriteString("[ERROR] " + msg + "\n")
	return err
}


//another logger

type StdLogger struct {
	logger *log.Logger
}

func NewStdLogger(path string) (*StdLogger, error){
	f, err := os.OpenFile(path, os.O_CREATE|os.O_APPEND|os.O_WRONLY, 0644)
	if err != nil {
		return nil, err
	}
	l := log.New(f, "", log.LstdFlags)
	return &StdLogger{logger: l}, nil

}


//adapter 
type StdLoggerAdapter struct {
	std *StdLogger
}

func NewStdLoggerAdapter(std *StdLogger) *StdLoggerAdapter {
	return &StdLoggerAdapter{std: std}
}

func (a *StdLoggerAdapter) Info(msg string) error {
	a.std.logger.SetPrefix("[INFO] ")
	a.std.logger.Println(msg)
	return nil
}


func (a *StdLoggerAdapter) Error(msg string) error {
	a.std.logger.SetPrefix("[ERROR] ")
	a.std.logger.Println(msg)
	return nil
}


func runApp(log Logger) {
	_ = log.Info("service started")
	_ = log.Error("null pr exception")	
}

func main() {

	fl, err := NewFileLogger("file.log")	
	if err != nil {
		log.Fatalf("file logger error: %v", err)
	}
	runApp(fl)

	std, err := NewStdLogger("stdlib.log")	
		if err != nil {
		log.Fatalf("stdlib logger error: %v", err)
	}
	stdAdapter := NewStdLoggerAdapter(std)
	runApp(stdAdapter)

}
```

### Goroutine-Safe Version

In real-world scenarios, logging typically involves concurrent writes from multiple goroutines. To avoid race conditions, thread safety is essential. Use synchronization primitives such as `sync.Mutex` to protect shared resources.  

```go
package main

import (
	"log"
	"os"
	"sync"
)

type Logger interface {
	Info(msg string) error
	Error(msg string) error
}

type FileLogger struct {
	file *os.File
	mu sync.Mutex
}


func NewFileLogger(path string) (*FileLogger, error) {
	f, err := os.OpenFile(path, os.O_CREATE|os.O_APPEND|os.O_WRONLY, 0644)
	if err != nil {
		return nil, err 
	}

	return &FileLogger{file: f}, nil
}


func (l *FileLogger) Info(msg string) error {
	l.mu.Lock()
	defer l.mu.Unlock()
	
	_, err := l.file.WriteString("[INFO] " + msg + "\n")
	return err
}
func (l *FileLogger) Error(msg string) error {
	l.mu.Lock()
	defer l.mu.Unlock()

	_, err := l.file.WriteString("[ERROR] " + msg + "\n")
	return err
}


//another logger

type StdLogger struct {
	logger *log.Logger
}

func NewStdLogger(path string) (*StdLogger, error){
	f, err := os.OpenFile(path, os.O_CREATE|os.O_APPEND|os.O_WRONLY, 0644)
	if err != nil {
		return nil, err
	}
	l := log.New(f, "", log.LstdFlags)
	return &StdLogger{logger: l}, nil

}


//adapter 
type StdLoggerAdapter struct {
	std *StdLogger
	mu sync.Mutex
}

func NewStdLoggerAdapter(std *StdLogger) *StdLoggerAdapter {
	return &StdLoggerAdapter{std: std}
}

func (a *StdLoggerAdapter) Info(msg string) error {
	a.mu.Lock()
	defer a.mu.Unlock()
	
	a.std.logger.SetPrefix("[INFO] ")
	a.std.logger.Println(msg)
	return nil
}


func (a *StdLoggerAdapter) Error(msg string) error {
	a.mu.Lock()
	defer a.mu.Unlock()
	
	a.std.logger.SetPrefix("[ERROR] ")
	a.std.logger.Println(msg)
	return nil
}


func runApp(log Logger) {
	_ = log.Info("service started")
	_ = log.Error("null pr exception")	
}

func main() {

	fl, err := NewFileLogger("file.log")	
	if err != nil {
		log.Fatalf("file logger error: %v", err)
	}
	runApp(fl)

	std, err := NewStdLogger("stdlib.log")	
		if err != nil {
		log.Fatalf("stdlib logger error: %v", err)
	}
	stdAdapter := NewStdLoggerAdapter(std)
	runApp(stdAdapter)

}
```

The Adapter pattern is useful in Golang because:

* **Improved Flexibility**: Easily integrate third-party libraries or legacy code.
    
* **Decoupling**: Client code remains unaware of underlying specific implementations.
    
* **Maintainability**: Easier to switch implementations later without modifying client code.
    

## Decorator

> **Decorator** is a structural design pattern that lets you attach new behaviors to objects by placing these objects inside special wrapper objects that contain the behaviors.

Imagine you have a simple `FileStorage` struct that directly saves and loads data from the file system. It has basic methods like `Save` and `Load` directly embedded into it.  

```go
package main

import (
	"fmt"
	"os"
)

type FileStorage struct {
	basePath string
}

func NewFileStorage(basePath string) *FileStorage {
	return &FileStorage{basePath: basePath}
}

func (fs *FileStorage) Save(filename string, data []byte) error {
	filePath := fs.basePath + "/" + filename
	return os.WriteFile(filePath, data, 0644)
}

func (fs *FileStorage) Load(filename string) ([]byte, error) {
	filePath := fs.basePath + "/" + filename
	return os.ReadFile(filePath)
}

func main() {
	fs := NewFileStorage("./")
	err := fs.Save("hello.txt", []byte("hello, world!"))
	if err != nil {
		panic(err)
	}
	data, err := fs.Load("hello.txt")
	if err != nil {
		panic(err)
	}
	fmt.Println("data: ", string(data))
}
```

### Problems With That Code

* **Inflexibility**: Difficult to add new behaviors (like compression, encryption, logging) without changing existing code.
    
* **Code Duplication**: Adding features requires repeating logic across different places.
    
* **Harder to Maintain**: Adding new features directly into methods increases complexity and reduces readability.
    

The **Decorator pattern** addresses these problems by wrapping the original object (Component) with decorators that add behaviors dynamically without altering the original object's code.

![](https://cdn.hashnode.com/res/hashnode/image/upload/v1751375902523/ecddf9ad-3d35-4c29-a60f-f354a2033cc2.png align="center")

According to the above diagram:

* The `Component` interface defines the basic operation (`execute()`).
    
* `Concrete Component` provides the default implementation.
    
* `Base Decorator` holds a reference (`wrappee`) to a component and delegates calls.
    
* `Concrete Decorators` add extra behavior (`extra()`) before or after delegating calls to the wrapped component.
    

This solves the earlier issues by allowing:

* Easy composition of multiple behaviors (e.g., logging + compression).
    
* Flexibility to add or remove behaviors dynamically at runtime.
    
* Keeping original implementations clean and simple.
    

### Code Using the Decorator Pattern

Implementing the Decorator pattern involves defining storage decorators like `LoggingStorage` and `CompressedStorage` that add extra behaviors dynamically without modifying underlying storage implementations.

```go
package main

import (
	"bytes"
	"compress/gzip"
	"fmt"
	"io"
	"log"
	"os"
)

type Storage interface {
	Save(filename string, data []byte) error
	Load(filename string) ([]byte, error) 
}


type FileStorage struct {
	basePath string	
}


func NewFileStorage(bp string) *FileStorage {
	return &FileStorage{basePath: bp}
}

func (fs *FileStorage) Save(filename string, data []byte) error {
	filePath := fs.basePath + "/" + filename
	return os.WriteFile(filePath, data, 0644)
}

func (fs *FileStorage) Load(filename string) ([]byte, error) {
	filePath := fs.basePath + "/" + filename
	return os.ReadFile(filePath)
}


//decorator

type LoggingStorage struct {
	inner Storage
}


func NewLogginStorage(inner Storage) *LoggingStorage {
	return &LoggingStorage{inner: inner}
}

func (ls *LoggingStorage) Save(filename string, data []byte) error{
	log.Printf("Saving file: %s (size: %d)", filename, len(data))
	err := ls.inner.Save(filename, data)
	if err != nil {
		log.Printf("Error saving file: %v", err)
	}
	return err
}


func (ls *LoggingStorage) Load(filename string) ([]byte, error) {
	log.Printf("Loading file: %s", filename)
	data, err := ls.inner.Load(filename)
	if err != nil {
		log.Printf("Error loading file: %v", err)
	}
	return data, err
}


//decorator

type CompressedStorage struct {
	inner Storage
}

func NewCompressedStorage(inner Storage) *CompressedStorage {
	return &CompressedStorage{inner: inner}
}

func (cs *CompressedStorage) Save(filename string, data []byte) error {
	var buf bytes.Buffer
	zw := gzip.NewWriter(&buf)
	_, err := zw.Write(data)
	if err != nil {
		return err
	}

	zw.Close()
	return cs.inner.Save(filename, buf.Bytes())
}

func (cs *CompressedStorage) Load(filename string) ([]byte, error) {
	compressed, err := cs.inner.Load(filename)
	if err != nil {
		return nil, err
	}

	zr, err := gzip.NewReader(bytes.NewReader(compressed))
	if err != nil {
		return nil, err
	}
	defer zr.Close()
	return io.ReadAll(zr)

}

func main() {
	_ = os.Mkdir("./", 0755)
	
	base := NewFileStorage("./")
	storage := NewLogginStorage(NewCompressedStorage(base))


	if err := storage.Save("green.txt", []byte("this data will be compressed")); err!= nil {
		panic(err)
	}

	data, err := storage.Load("green.txt")	
	if err != nil {
		panic(err)
	}

	fmt.Println("data: ", string(data))

}
```

### Goroutine-Safe Version

In concurrent applications, decorators and underlying objects should be thread-safe to avoid race conditions. You can achieve goroutine safety by using synchronization primitives like `sync.Mutex` within your implementations. (Put your provided goroutine-safe decorator Go code here.)

The Decorator pattern is powerful for Go developers due to its:

* **High flexibility**: Dynamically combine behaviors at runtime.
    
* **Separation of concerns**: Core logic remains unchanged, enhancing maintainability.
    
* **Improved readability and testability**: Each decorator is isolated and easy to test.
    

## Proxy

> **Proxy** is a structural design pattern that lets you provide a substitute or placeholder for another object. A proxy controls access to the original object, allowing you to perform something either before or after the request gets through to the original object.

Suppose you're directly using an HTTP client (`RealHTTPClient`) in your application to make web requests. Each request directly reaches the external server.  

```go
package main

import (
	"fmt"
	"io"
	"net/http"
	"time"
)

type HTTPClient interface {
	Do(req *http.Request) (*http.Response, error)
}

type RealHTTPClient struct {
	client *http.Client
}

func NewRealHttpClient(timeout time.Duration) *RealHTTPClient{
	return &RealHTTPClient{
		client: &http.Client{
			Timeout: timeout,
		},
	}
}

func (c *RealHTTPClient) Do(req *http.Request) (*http.Response, error) {
	return c.client.Do(req)
} 

func main() {
	client := NewRealHttpClient(5 * time.Second)
	req, err := http.NewRequest("GET", "https://example.com", nil)
	if err != nil {
		panic(err)
	}
	resp, err := client.Do(req)
	if err != nil {
		panic(err)
	}

	defer resp.Body.Close()
	data, err := io.ReadAll(resp.Body)
	if err != nil{
		panic(err)
	}

	fmt.Println("data: ", string(data))
}
```

### Problems With That Code

* **Uncontrolled Access**: Every call hits external services directly, causing potential rate-limit or performance issues.
    
* **Limited Control**: Hard to add caching, rate limiting, logging, or other behaviors without modifying the client code.
    
* **Inflexibility**: Changing or adding behavior requires extensive code modifications.
    

The **Proxy Pattern** solves these problems by placing an intermediate object (Proxy) between the client and the real service. This proxy controls access to the real object, handling tasks such as access checks, rate-limiting, caching, or logging.  

![](https://cdn.hashnode.com/res/hashnode/image/upload/v1751375986283/7cfa35ce-04c2-4583-aa4b-4064e2793122.png align="center")

* `Client` uses a common `ServiceInterface` instead of directly accessing the real object.
    
* `Proxy` implements this interface, holding a reference (`realService`) to the real object.
    
* Proxy intercepts calls, performing additional actions (`checkAccess`) before delegating to the real object.
    

This solves the earlier problems by allowing:

* **Controlled Access**: Implementing additional checks or limits transparently.
    
* **Improved Maintainability**: Adding new behavior without modifying existing client or service code.
    
* **Flexible Enhancements**: Easy extension of functionality like caching, authentication, or rate limiting.
    

### Code Using the Proxy Pattern

Implementing a proxy like `RateLimitProxy` allows controlling how frequently your HTTP client can make external requests. The proxy sits between the client and the real HTTP client, enforcing access control.

```go
package main

import (
	"fmt"
	"io"
	"net/http"
	"sync"
	"time"
)

type HTTPClient interface {
	Do(req *http.Request) (*http.Response, error)
}

type RealHTTPClient struct {
	client *http.Client
}

func NewRealHttpClient(timeout time.Duration) *RealHTTPClient{
	return &RealHTTPClient{
		client: &http.Client{
			Timeout: timeout,
		},
	}
}

func (c *RealHTTPClient) Do(req *http.Request) (*http.Response, error) {
	return c.client.Do(req)
} 


type RateLimitProxy struct {
	real HTTPClient
	interval time.Duration
	lastReq time.Time
	mu sync.Mutex
}


func NewRateLimitProxy(real HTTPClient, perSecond int) *RateLimitProxy{
	return &RateLimitProxy{
		real: real,
		interval: time.Second / time.Duration(perSecond),
	}
}

func (p *RateLimitProxy) Do(req *http.Request) (*http.Response, error) {
	p.mu.Lock()
	now := time.Now()
	wait := p.lastReq.Add(p.interval).Sub(now)
	if wait > 0 {
		p.mu.Unlock()
		time.Sleep(wait)
		p.mu.Lock()
	}
	p.lastReq = time.Now()
	p.mu.Unlock()
	return p.real.Do(req)
}


func main() {
	client := NewRealHttpClient(5 * time.Second)
	rateLimiter := NewRateLimitProxy(client, 2)


	for range 5 {
		req, err := http.NewRequest("GET", "https://example.com", nil)
		if err != nil {
			panic(err)
		}
		resp, err := rateLimiter.Do(req)
		if err != nil {
			panic(err)
		}

		defer resp.Body.Close()
		data, err := io.ReadAll(resp.Body)
		if err != nil{
			panic(err)
		}

		fmt.Println("data: ", string(data))
	}

	
}
```

### Goroutine-Safe Version

When multiple goroutines make requests concurrently, proxies must handle synchronization and thread safety. Using channels (token-bucket method) or mutexes ensures safe concurrent access without race conditions..  

```go
package main

import (
	"fmt"
	"io"
	"net/http"
	"sync"
	"time"
)

type HTTPClient interface {
	Do(req *http.Request) (*http.Response, error)
}

type RealHTTPClient struct {
	client *http.Client
}

func NewRealHttpClient(timeout time.Duration) *RealHTTPClient{
	return &RealHTTPClient{
		client: &http.Client{
			Timeout: timeout,
		},
	}
}

func (c *RealHTTPClient) Do(req *http.Request) (*http.Response, error) {
	return c.client.Do(req)
} 


type RateLimitProxy struct {
	real HTTPClient
	tokens chan struct{}
}


func NewRateLimitProxy(real HTTPClient, perSecond int) *RateLimitProxy{
	p := &RateLimitProxy{
		real: real,
		tokens: make(chan struct{}, perSecond),
	}

	go func(){
		ticker := time.NewTicker(time.Second/ time.Duration(perSecond))
		defer ticker.Stop()
		for {
			<-ticker.C
			select{
			case p.tokens <- struct{}{}:
			//bucket is full
			default:
			}
		}
	}()

	return p
}

func (p *RateLimitProxy) Do(req *http.Request) (*http.Response, error) {
	<-p.tokens
	return p.real.Do(req)
}


func main() {
	client := NewRealHttpClient(5 * time.Second)
	rateLimiter := NewRateLimitProxy(client, 3)

	var wg sync.WaitGroup
	for i := 0; i < 10; i++ {
		wg.Add(1)

		go func(i int){
			defer wg.Done()

			req, err := http.NewRequest("GET", "https://example.com", nil)
			if err != nil {
				panic(err)
			}
			resp, err := rateLimiter.Do(req)
			if err != nil {
				panic(err)
			}

			defer resp.Body.Close()
			_, err = io.ReadAll(resp.Body)
			if err != nil{
				panic(err)
			}

			fmt.Println("request: ", i)

		}(i)


		
	}

	wg.Wait()

	
}
```

The Proxy pattern provides several advantages for Go developers:

* **Improved Control**: Easy implementation of features like rate-limiting, authentication, and caching.
    
* **Separation of Concerns**: Clearly separates service usage logic from access-control logic.
    
* **Enhanced Flexibility**: Changing proxy behavior doesn't require modifications in client or original service implementations.
    

However, in very simple use cases, adding a proxy might unnecessarily complicate your codebase. It's ideal when you need additional access control or functionalities transparently.

## Composite

> **Composite** is a structural design pattern that lets you compose objects into tree structures and then work with these structures as if they were individual objects.

Imagine you're representing a file directory using a `Folder` struct directly holding files and other folders. This requires separate logic for files and folders, making handling complex structures cumbersome.

```go
package main

import "fmt"

type Folder struct  {
	Name string
	Files []string
	Children []*Folder
}


func printTree(folder *Folder, indent string) {
	fmt.Printf("%s[%s]\n", indent, folder.Name)
	for _, f := range folder.Files {
		fmt.Printf("%s  - %s\n", indent, f)
	}
	for _, child := range folder.Children {
		printTree(child, indent+"  ")
	}
}


func countFiles(folder *Folder) int {
	count := len(folder.Files)
	for _, child := range folder.Children {
		count += countFiles(child)
	}

	return count
}


func main() {

	root := &Folder{
		Name: "root",
		Files: []string{"README.md"},
		Children: []*Folder {
			{
				Name: "src",
				Files: []string{"main.go", "utils.go"},
			},
			{
				Name: "assets",
				Files: []string{"logo.png"},	
				Children: []*Folder{
					{
						Name: "icons",
						Files: []string{"icon.svg"},
				
					},

				},
			},
		},
	}

	printTree(root, "")
	fmt.Println("total files: ", countFiles(root))

}
```

### Problems With That Code

* **Complexity**: Logic to manage nested folders and files gets complicated.
    
* **Tight coupling**: Separate handling of files and folders requires extensive branching.
    
* **Lack of scalability**: Adding new types of components (like links) requires changes in multiple places.
    

The **Composite Pattern** simplifies working with hierarchical structures (like file systems) by treating individual objects and compositions uniformly.

![](https://cdn.hashnode.com/res/hashnode/image/upload/v1751376095507/07025c9f-9e8c-4f78-818d-2f47d6124137.png align="center")

* The `Component` interface declares common operations (`execute`).
    
* `Leaf` represents individual objects (e.g., files) and directly performs operations.
    
* `Composite` represents complex components (e.g., folders) containing children and delegates operations to them.
    
* `Client` interacts with both composites and leaves via the common interface, unaware of their exact type.
    

This solves earlier issues by:

* Allowing uniform treatment of single objects and compositions.
    
* Simplifying client code and reducing branching logic.
    
* Making it easier to scale and extend the structure.
    

### Code Using the Composite Pattern

Implementing the Composite pattern involves creating a common interface (`Node`) for both files (`Leaf`) and folders (`Composite`) and allowing clients to treat them uniformly.  

```go
package main

import "fmt"

//conponent
type Node interface {
	Print(indent string)
	CountFiles() int
	Name() string
}


//leaf

type File struct {
	name string
}


func (f *File) Print(indent string) {
	fmt.Printf("%s- %s\n", indent, f.name)
}


func (f *File) CountFiles() int {
	return 1
}

func (f *File) Name() string {
	return f.name
}


//composite

type Folder struct {
	name string
	children []Node
}


func (d *Folder) Print(indent string) {
	fmt.Printf("%s[%s]\n", indent, d.name)
	for _, child := range d.children {
		child.Print(indent + " ")
	}
}

func (d *Folder) CountFiles() int {
	total := 0
	for _, child := range d.children {
		total += child.CountFiles()
	}

	return total
}

func (d *Folder) Name() string {
	return d.name
}


func main() {
	root := &Folder{name: "root"}
	src := &Folder{name: "src"}
	assets := &Folder{name: "assets"}
	icons := &Folder{name: "icons"}

	// Compose tree
	src.children = append(src.children, &File{name: "main.go"}, &File{name: "utils.go"})
	icons.children = append(icons.children, &File{name: "icon.svg"})
	assets.children = append(assets.children, &File{name: "logo.png"}, icons)
	root.children = append(root.children, &File{name: "README.md"}, src, assets)

	root.Print("")
	fmt.Println("Total files:", root.CountFiles())
}
```

### Goroutine-Safe Version

In real-world applications, components might be accessed concurrently. To handle concurrent operations safely, use synchronization primitives like `sync.RWMutex` to protect shared structures.  

```go
package main

import (
	"fmt"
	"sync"
)

//conponent
type Node interface {
	Print(indent string)
	CountFiles() int
	Name() string
	Add(child Node)
}


//leaf

type File struct {
	name string
}


func (f *File) Print(indent string) {
	fmt.Printf("%s- %s\n", indent, f.name)
}


func (f *File) CountFiles() int {
	return 1
}

func (f *File) Name() string {
	return f.name
}


func (f *File) Add(child Node ) {
	//nothin
}

//composite

type Folder struct {
	name string
	mu sync.RWMutex
	children []Node
}


func (d *Folder) Print(indent string) {
	fmt.Printf("%s[%s]\n", indent, d.name)
	d.mu.RLock()
	defer d.mu.RUnlock()
	for _, child := range d.children {
		child.Print(indent + " ")
	}
}

func (d *Folder) CountFiles() int {
	d.mu.RLock()
	defer d.mu.RUnlock()
	total := 0
	for _, child := range d.children {
		total += child.CountFiles()
	}

	return total
}

func (d *Folder) Name() string {
	return d.name
}


func (d *Folder) Add(child Node) {
	d.mu.RLock()
	defer d.mu.RUnlock()
	d.children = append(d.children, child)
}


func main() {
	root := &Folder{name: "root"}
	src := &Folder{name: "src"}
	assets := &Folder{name: "assets"}
	icons := &Folder{name: "icons"}

	src.Add(&File{name: "main.go"})
	src.Add(&File{name: "utils.go"})
	icons.Add(&File{name: "icon.svg"})
	assets.Add(&File{name: "logo.png"})
	assets.Add(icons)
	root.Add(&File{name: "README.md"})
	root.Add(src)
	root.Add(assets)

	root.Print("")
	fmt.Println("Total files:", root.CountFiles())


	var wg sync.WaitGroup
	for i := 0; i < 10; i++ {
		wg.Add(1)
		go func(n int) {
			defer wg.Done()
			root.Add(&File{name: fmt.Sprintf("concurrent-%d.txt", n)})
		}(i)
	}
	wg.Wait()
	fmt.Println("After concurrent add:")
	root.Print("")
	fmt.Println("Total files:", root.CountFiles())



}
```

The Composite pattern is highly beneficial for Go developers:

* **Simplifies Client Code**: Clients don’t need to differentiate between leaves and composites.
    
* **Flexibility and Scalability**: Easy to add new types of components without extensive code changes.
    
* **Maintainability**: Clearly defines structure and responsibilities.
    

However, if your structures are simple or flat, using Composite might add unnecessary complexity. It's ideal for hierarchical data structures.  

---

# Behavioral Design Patterns

Behavioral design patterns provide solutions for effective communication and clear separation of responsibilities among objects. They deal with object collaboration, defining how tasks and interactions should be distributed to achieve loose coupling and high cohesion in your Go applications. By clearly managing behaviors and responsibilities, these patterns help you create applications that are easier to test, debug, and extend.

This section introduces patterns that streamline object interaction, event handling, and state management, ensuring clean and maintainable logic flow in your applications.

## Strategy

> **Strategy** is a behavioral design pattern that lets you define a family of algorithms, put each of them into a separate class, and make their objects interchangeable.

Imagine you’re building a file-saving utility with different compression algorithms (gzip, zlib, none). In a naive implementation, you'd directly use conditional logic (`switch-case`) to choose compression methods.  

```go
package main

import (
	"bytes"
	"compress/gzip"
	"compress/zlib"
	"errors"
	"os"
)

func compressGzip(data []byte) ([]byte, error) {
	var buf bytes.Buffer
	gz := gzip.NewWriter(&buf)
	_, err := gz.Write(data)

	if err != nil {
		return nil, err
	}
	if err := gz.Close(); err != nil{
		return nil, err
	}

	return buf.Bytes(), nil

}

func compressZlib(data []byte)([]byte, error){
	var buf bytes.Buffer
	zw := zlib.NewWriter(&buf)
	_, err := zw.Write(data)
	if err != nil {
		return nil, err
	}
	err = zw.Close()
	if err != nil {
		return nil, err
	}

	return buf.Bytes(), nil

}


func compressNone(data []byte) ([]byte, error) {
	return data, nil
}


func saveCompressedFile(path, algo string, data []byte) error {
	var compressed []byte
	var err error

	switch algo {
	case "gzip":
		compressed, err = compressGzip(data)
	case "zlib":
		compressed, err = compressZlib(data)
	case "none":
		compressed, err = compressNone(data)
	default:
		return errors.New("unknown algo")
	}

	if err != nil {
		return err
	}
	f, err := os.Create(path)
	if err != nil {
		return err
	}

	defer f.Close()

	_, err = f.Write(compressed)
	return err

}


func main() {
	content := []byte("hllo this is strategy pattern in golang!")

	_ = saveCompressedFile("file.gz", "gzip", content)
	_ = saveCompressedFile("file.zlib", "zlib", content)
	_ = saveCompressedFile("file.raw", "none", content)


}
```

### Problems With That Code

* **Hard to maintain**: Adding new algorithms requires modifying existing code.
    
* **Code Duplication**: Similar compression logic might be repeated in multiple places.
    
* **Lack of Flexibility**: Hard to switch algorithms at runtime or reuse logic elsewhere.
    

The **Strategy pattern** separates algorithms into distinct classes (`ConcreteStrategies`) implementing a common interface (`Strategy`). The client (`Context`) holds a reference to a strategy object and delegates the execution to this object, making algorithms interchangeable at runtime.

![](https://cdn.hashnode.com/res/hashnode/image/upload/v1751376205468/23f1c300-da18-483b-9b9c-c46da7116552.png align="center")

According to the above diagram:

* `Context` class holds a reference to a `Strategy`.
    
* `Strategy` interface declares a common operation (`execute()`).
    
* `ConcreteStrategies` implement the operation differently.
    
* `Client` dynamically sets strategies on the context to perform actions.
    

This resolves earlier issues by:

* Allowing easy addition or modification of algorithms without affecting client code.
    
* Providing flexibility to switch algorithms dynamically at runtime.
    
* Improving maintainability by clearly separating algorithm logic from application logic.
    

### Code Using the Strategy Pattern

Implementing Strategy involves defining a `Compressor` interface, concrete implementations (`GzipCompressor`, `ZlibCompressor`, etc.), and a context (`FileSaver`) using these strategies interchangeably.

```go
package main

import (
	"bytes"
	"compress/gzip"
	"compress/zlib"
	"errors"
	"os"
)

type Compressor interface {
	Compress([]byte) ([]byte, error)
}


//concrete strategy

type GzipCompressor struct{}

func (GzipCompressor) Compress(data []byte) ([]byte, error) {
	var buf bytes.Buffer
	gz := gzip.NewWriter(&buf)
	_, err := gz.Write(data)
	if err != nil {
		return nil, err
	}
	if err := gz.Close(); err != nil {
		return nil, err
	}

	return buf.Bytes(), nil
}

type ZlibCompressor struct{}

func (ZlibCompressor) Compress(data []byte) ([]byte, error) {
	var buf bytes.Buffer
	zw := zlib.NewWriter(&buf)
	_, err := zw.Write(data)
	if err != nil {
		return nil, err
	}

	if err := zw.Close(); err != nil {
		return nil, err
	}

	return buf.Bytes(), nil
}


type NoCompressor struct{}

func (NoCompressor) Compress(data []byte) ([]byte, error) {
	return data, nil
}

//context, aka object using strategy

type FileSaver struct {
	Compressor Compressor
}


func (fs *FileSaver) Save(path string, data []byte) error {
	
	compressed, err := fs.Compressor.Compress(data)
	if err != nil {
		return err
	}

	f, err := os.Create(path)
	if err != nil{
		return err
	}
	defer f.Close()
	_, err = f.Write(compressed)
	return err
	
	
}


func CompressorFactory( algo string) (Compressor, error) {

	switch algo {
	case "gzip":
		return GzipCompressor{}, nil
	case "zlib":
		return ZlibCompressor{}, nil
	case "none":
		return NoCompressor{}, nil
	default:
		return nil,  errors.New("unknown algo")
	}


}



func main() {

	content := []byte("Hello, World! Strategy Pattern Example.")

	gz, _ := CompressorFactory("gzip")	
	fs := &FileSaver{Compressor: gz}
	_ = fs.Save("file.gz", content)
	

	zlib, _ := CompressorFactory("zlib")	
	fs.Compressor = zlib
	_ = fs.Save("file.zlib", content)

	none, _ := CompressorFactory("none")	
	fs.Compressor = none
	_ = fs.Save("file.raw", content)


}
```

### Goroutine-Safe Version

For thread-safe strategy switching and usage in concurrent environments, use synchronization techniques like `sync.RWMutex` to safely modify or access the strategy objects.  

```go
package main

import (
	"bytes"
	"compress/gzip"
	"compress/zlib"
	"errors"
	"os"
	"sync"
)

type Compressor interface {
	Compress([]byte) ([]byte, error)
}


//concrete strategy

type GzipCompressor struct{}

func (GzipCompressor) Compress(data []byte) ([]byte, error) {
	var buf bytes.Buffer
	gz := gzip.NewWriter(&buf)
	_, err := gz.Write(data)
	if err != nil {
		return nil, err
	}
	if err := gz.Close(); err != nil {
		return nil, err
	}

	return buf.Bytes(), nil
}

type ZlibCompressor struct{}

func (ZlibCompressor) Compress(data []byte) ([]byte, error) {
	var buf bytes.Buffer
	zw := zlib.NewWriter(&buf)
	_, err := zw.Write(data)
	if err != nil {
		return nil, err
	}

	if err := zw.Close(); err != nil {
		return nil, err
	}

	return buf.Bytes(), nil
}


type NoCompressor struct{}

func (NoCompressor) Compress(data []byte) ([]byte, error) {
	return data, nil
}

//context, aka object using strategy

type FileSaver struct {
	mu sync.RWMutex
	Compressor Compressor
}

//safe set

func (fs *FileSaver) SetCompressor(c Compressor) {
	fs.mu.Lock()
	defer fs.mu.Unlock()
	fs.Compressor = c
}


func (fs *FileSaver) Save(path string, data []byte) error {
	
	fs.mu.RLock()
	c := fs.Compressor
	fs.mu.RUnlock()

	compressed, err := c.Compress(data)
	if err != nil {
		return err
	}

	f, err := os.Create(path)
	if err != nil{
		return err
	}
	defer f.Close()
	_, err = f.Write(compressed)
	return err
	
	
}


func CompressorFactory( algo string) (Compressor, error) {

	switch algo {
	case "gzip":
		return GzipCompressor{}, nil
	case "zlib":
		return ZlibCompressor{}, nil
	case "none":
		return NoCompressor{}, nil
	default:
		return nil,  errors.New("unknown algo")
	}


}



func main() {

	content := []byte("Hello, World! Strategy Pattern Example.")

	algos := []string{"gzip", "zlib", "none"}
	files := []string{"file-safe.gz", "file-safe.zlib", "file-safe.raw"}

	fs := &FileSaver{}
	wg := sync.WaitGroup{}

	for i, algo := range algos {
		comp, _ := CompressorFactory(algo)
		fs.SetCompressor(comp)

		wg.Add(1)
		go func(path string, data []byte) {
			defer wg.Done()
			err := fs.Save(path, data)
			if err != nil {
				panic(err)
			}

		}(files[i], content)
	}

	wg.Wait()

}
```

The Strategy pattern provides key benefits for Go developers:

* **Flexible and dynamic algorithm swapping**: Easily change or extend behavior without extensive refactoring.
    
* **Reduced complexity and cleaner code**: Separates concerns clearly, improving readability and maintainability.
    
* **Improved Testability**: Easier to mock or replace strategies for unit testing.
    

## Observer

> **Observer** is a behavioral design pattern that lets you define a subscription mechanism to notify multiple objects about any events that happen to the object they're observing.

Imagine you're building an application that manages configuration changes. Each time a config changes, you manually update dependent components like a logger or a cache explicitly in the application logic.  

```go
package main

import (
	"fmt"
	"os"
)

type Config struct {
	LogLevel string	
}


type Cache struct {
	data map[string]string
}


func (c *Cache) Update (cfg *Config) {
	c.data["log_level"] = cfg.LogLevel
}



type Logger struct {
	level string
}


func (l *Logger) SetLevel(level string) {
	l.level = level
}	

type App struct {
	config *Config
	cache  *Cache
	logger *Logger
}


func LoadConfig(path string) (*Config, error) {
	b, err := os.ReadFile(path)
	if err != nil {
		return nil, err
	}

	return &Config{LogLevel: string(b)},nil
}


func (a *App) ReloadConfig(path string) error {
	cfg, err := LoadConfig(path)
	if err != nil {
		return err
	}

	a.config = cfg

	a.cache.Update(cfg)
	a.logger.SetLevel(cfg.LogLevel)
	return nil
}



func main() {

	cache := &Cache{data: make(map[string]string)}
	logger := &Logger{}
	app := &App{cache: cache, logger: logger}


	//initial cinfig load
	_ = os.WriteFile("config.txt", []byte("INFO"), 0644)
	_ = app.ReloadConfig("config.txt")

	//config change
	_ = os.WriteFile("config.txt", []byte("DEBUG"), 0644)
	_ = app.ReloadConfig("config.txt")

	fmt.Println(app.logger.level)
	fmt.Println(app.cache.data["log_level"])


}
```

### Problems With That Code

* **Tight Coupling**: Components that depend on the configuration are directly referenced and managed explicitly.
    
* **Hard to Extend**: Adding new observers (components) requires modifications in multiple locations.
    
* **Difficult to Maintain**: Updates propagate manually, increasing the risk of inconsistency.
    

The **Observer pattern** introduces a mechanism for subscribers (`Observers`) to register with a publisher (`Subject`). Whenever an event or state change occurs in the publisher, all subscribers are automatically notified.

![](https://cdn.hashnode.com/res/hashnode/image/upload/v1751376354862/42e5b5ce-fe37-4383-a4c1-e87cf9cacbdb.png align="center")

* `Publisher` maintains a list of subscribers (`Subscriber` interface) and the state (`mainState`).
    
* Subscribers implement the `Subscriber` interface and define the `update(context)` method.
    
* `Concrete Subscribers` are registered with the publisher.
    
* Whenever a change occurs, the publisher notifies all subscribers by calling their `update()` methods.
    

This resolves the earlier issues by:

* Providing loose coupling between publishers and subscribers.
    
* Simplifying the addition of new subscribers.
    
* Ensuring consistent and automatic updates.
    

### Code Using the Observer Pattern

Implementing the Observer pattern in Go involves creating a `ConfigObserver` interface and registering concrete observers (like `Logger` and `Cache`) with the publisher (`ConfigLoader`).

```go
package main

import (
	"fmt"
	"os"
)

type COnfig struct {
	LogLevel string	
}


type ConfigObserver interface {
	OnConfigChange(cfg *COnfig)
}

type ConfigLoader struct {
	config *COnfig
	observers []ConfigObserver
}


func NewConfigLoader() *ConfigLoader {
	return &ConfigLoader{
		observers: make([]ConfigObserver, 0),
	}
}

func (cl *ConfigLoader) RegisterObserver(obs ConfigObserver) {
	cl.observers = append(cl.observers, obs)
}


func (cl *ConfigLoader) LoadConfig(path string) error {
	b, err := os.ReadFile(path)
	if err != nil {
		return err
	}

	cfg := &COnfig{LogLevel: string(b)}
	cl.config = cfg
	cl.notifyAll(cfg)
	return nil
}

func (cl *ConfigLoader) notifyAll(cfg *COnfig) {
	for _, obs := range cl.observers {
		obs.OnConfigChange(cfg)
	}
}

//observers

type Cache struct {
	data map[string]string
}

func (c *Cache) OnConfigChange (cfg *COnfig)	 {
	c.data["log_level"] = cfg.LogLevel
}

type Logger struct {
	level string
}

func (l *Logger) OnConfigChange (cfg *COnfig) {
	l.level = cfg.LogLevel
}


func main() {

	cache := &Cache{data: make(map[string]string)}
	logger := &Logger{}

	cl := NewConfigLoader()
	cl.RegisterObserver(cache)
	cl.RegisterObserver(logger)


	_ = os.WriteFile("config.txt", []byte("INFO"), 0644)
	_ = cl.LoadConfig("config.txt")

	fmt.Println(logger.level)
	fmt.Println(cache.data["log_level"])

	_ = os.WriteFile("config.txt", []byte("DEBUG"), 0644)
	_ = cl.LoadConfig("config.txt")

	fmt.Println(logger.level)
	fmt.Println(cache.data["log_level"])

}
```

### Goroutine-Safe Version

In concurrent scenarios, observers and publishers might be accessed simultaneously. Thread safety can be achieved by synchronizing observer registrations and state changes using `sync.RWMutex`.

```go
package main

import (
	"fmt"
	"os"
	"sync"
)

type COnfig struct {
	LogLevel string	
}


type ConfigObserver interface {
	OnConfigChange(cfg *COnfig)
}

type ConfigLoader struct {
	mu sync.RWMutex
	config *COnfig
	observers []ConfigObserver
}


func NewConfigLoader() *ConfigLoader {
	return &ConfigLoader{
		observers: make([]ConfigObserver, 0),
	}
}

func (cl *ConfigLoader) RegisterObserver(obs ConfigObserver) {
	cl.mu.Lock()
	defer cl.mu.Unlock()
	
	cl.observers = append(cl.observers, obs)
}


func (cl *ConfigLoader) LoadConfig(path string) error {
	b, err := os.ReadFile(path)
	if err != nil {
		return err
	}
	cfg := &COnfig{LogLevel: string(b)}
	cl.mu.Lock()
	cl.config = cfg
	obsCopy := make([]ConfigObserver, len(cl.observers))
	copy(obsCopy, cl.observers)
	cl.mu.Unlock()

	for _, obs := range obsCopy {
		obs.OnConfigChange(cfg)
	}
	return nil
}


//observers

type Cache struct {
	mu sync.RWMutex
	data map[string]string
}

func (c *Cache) OnConfigChange (cfg *COnfig)	 {
	c.mu.Lock()
	defer c.mu.Unlock()
	c.data["log_level"] = cfg.LogLevel
}

type Logger struct {
	mu sync.RWMutex
	level string
}

func (l *Logger) OnConfigChange (cfg *COnfig) {
	l.mu.Lock()
	defer l.mu.Unlock()
	l.level = cfg.LogLevel
}


func main() {

	cache := &Cache{data: make(map[string]string)}
	logger := &Logger{}

	cl := NewConfigLoader()
	cl.RegisterObserver(cache)
	cl.RegisterObserver(logger)


	_ = os.WriteFile("config.txt", []byte("INFO"), 0644)
	_ = cl.LoadConfig("config.txt")

	fmt.Println(logger.level)
	fmt.Println(cache.data["log_level"])

	_ = os.WriteFile("config.txt", []byte("DEBUG"), 0644)
	_ = cl.LoadConfig("config.txt")

	cache.mu.RLock()
	fmt.Println(cache.data["log_level"])
	cache.mu.RUnlock()

	logger.mu.RLock()
	fmt.Println(logger.level)
	logger.mu.RUnlock()

}
```

The Observer pattern is highly beneficial in Go:

* **Loose coupling**: Observers and subjects don't need explicit knowledge about each other.
    
* **Extensibility**: Easy to add or remove subscribers without modifying the publisher’s logic.
    
* **Maintainability**: Reduces complexity by centralizing event notification.
    

It's ideal when multiple objects must remain synchronized with changes in a single object's state.

## Command

> **Command** is a behavioral design pattern that turns a request into a stand-alone object containing all information about the request. This transformation lets you pass requests as method arguments, delay or queue a request’s execution, and support undoable operations.

Imagine you directly manage file operations (create, rename, delete) using methods of a `FileManager` struct explicitly in a sequence.  

```go
package main

import (
	"os"
	"time"
)


type FileManager  struct{}

func (fm *FileManager) CreateFile(name string) error {
	_, err := os.Create(name)
	return err
}


func (fm *FileManager) DeleteFile(name string) error {
	return os.Remove(name)
}

func (fm *FileManager) RenameFile(oldname, newName string) error {
	return  os.Rename(oldname, newName)
}


func main() {

	manager := &FileManager{}

	if err := manager.CreateFile("test.txt"); err != nil {
		panic(err)
	}

	time.Sleep(time.Second * 3)

	if err := manager.RenameFile("test.txt", "results.txt"); err != nil {
		panic(err)
	}

	time.Sleep(time.Second * 3)

	if err := manager.DeleteFile("results.txt"); err != nil {
		panic(err)
	}	

}
```

### Problems With That Code

* **Tight Coupling**: Directly calling methods ties the invoking code closely to the file operations.
    
* **Lack of Flexibility**: Hard to queue, log, or rollback operations without extra complexity.
    
* **Difficult to Extend**: Introducing new operations or modifying existing sequences means modifying many parts of the codebase.
    

The **Command pattern** encapsulates requests as objects. This encapsulation allows commands to be queued, delayed, logged, or executed conditionally.

![](https://cdn.hashnode.com/res/hashnode/image/upload/v1751376467740/9ccbda0a-fd3d-47a0-8f51-d8b3cb3bd765.png align="center")

* `Command` interface defines an operation (`execute()`).
    
* `ConcreteCommand` binds the command with a specific receiver and parameters.
    
* `Invoker` stores and executes commands without knowing their concrete implementation.
    
* `Receiver` carries out the actual operations requested by commands.
    
* `Client` creates commands and associates them with receivers.
    

This resolves the earlier issues by:

* Decoupling request logic (commands) from execution logic (invoker and receiver).
    
* Providing flexibility for queuing, delaying, or logging commands.
    
* Enabling easy addition or removal of commands without impacting existing code.
    

### Code Using the Command Pattern

Implementing the Command pattern in Go involves defining a `Command` interface, creating concrete commands (`CreateCommand`, `RenameCommand`, `DeleteCommand`), and executing them via an invoker (`CommandQueue`).

```go
package main

import "os"

//command
type Command interface {
	Execute() error
}

//receier

type FileManager struct {}

func (fm *FileManager) CreateFile(name string) error {
	_, err := os.Create(name)
	return err
}


func (fm *FileManager) DeleteFile(name string) error {
	return os.Remove(name)
}

func (fm *FileManager) RenameFile(oldname, newName string) error {
	return  os.Rename(oldname, newName)
}

//concrete cmds

type CreateCommand struct {
	manager *FileManager
	name string
}


func (c *CreateCommand) Execute() error {
	return c.manager.CreateFile(c.name)
}


type DeleteCommand struct {
	manager *FileManager
	name string
}

func (c *DeleteCommand) Execute() error {
	return c.manager.DeleteFile(c.name)
}


type RenameCommand struct {
	manager *FileManager
	oldName string
	newName string
}


func (c *RenameCommand) Execute() error{
	return c.manager.RenameFile(c.oldName, c.newName)
}


//invoker

type CommandQueue struct {
	queue []Command
}


func (cq *CommandQueue) AddCommand(cmd Command) {
	cq.queue = append(cq.queue, cmd)
}


func (cq *CommandQueue) ExecuteAll() error {
	for _, cmd := range cq.queue {
		if err := cmd.Execute(); err  != nil {
			return err
		}
	}

	return nil
}


func main() {
	manager := &FileManager{}	

	queue := &CommandQueue{}

	queue.AddCommand(&CreateCommand{manager: manager, name: "test.txt"})
	queue.AddCommand(&RenameCommand{manager: manager, oldName: "test.txt", newName: "result.txt"})
	queue.AddCommand(&DeleteCommand{manager: manager, name: "result.txt"})

	if err := queue.ExecuteAll(); err != nil {
		panic(err)
	}


}
```

### Goroutine-Safe Version

For safe concurrent command execution, synchronize access to the command queue using `sync.Mutex`. Executing commands concurrently requires managing synchronization to avoid data races.

```go
package main

import (
	"os"
	"sync"
)

//command
type Command interface {
	Execute() error
}

//receier

type FileManager struct {}

func (fm *FileManager) CreateFile(name string) error {
	_, err := os.Create(name)
	return err
}


func (fm *FileManager) DeleteFile(name string) error {
	return os.Remove(name)
}

func (fm *FileManager) RenameFile(oldname, newName string) error {
	return  os.Rename(oldname, newName)
}

//concrete cmds

type CreateCommand struct {
	manager *FileManager
	name string
}


func (c *CreateCommand) Execute() error {
	return c.manager.CreateFile(c.name)
}


type DeleteCommand struct {
	manager *FileManager
	name string
}

func (c *DeleteCommand) Execute() error {
	return c.manager.DeleteFile(c.name)
}


type RenameCommand struct {
	manager *FileManager
	oldName string
	newName string
}


func (c *RenameCommand) Execute() error{
	return c.manager.RenameFile(c.oldName, c.newName)
}


//invoker

type CommandQueue struct {
	mu sync.Mutex
	queue []Command
}


func (cq *CommandQueue) AddCommand(cmd Command) {
	cq.mu.Lock()
	defer cq.mu.Unlock()
	cq.queue = append(cq.queue, cmd)
}


type CommandResult struct {
	Command Command
	Err     error
}


func (cq *CommandQueue) ExecuteAll() []CommandResult {
	cq.mu.Lock()
	defer cq.mu.Unlock()

	var results []CommandResult
	for _, cmd := range cq.queue {
		err := cmd.Execute()
		results = append(results, CommandResult{Command: cmd, Err: err})
	}

	cq.queue = nil 
	return results
}



func main() {
	manager := &FileManager{}	
	queue := &CommandQueue{}

	var wg sync.WaitGroup

	queue.AddCommand(&CreateCommand{manager: manager, name: "test.txt"})
	queue.AddCommand(&RenameCommand{manager: manager, oldName: "test.txt", newName: "result.txt"})
	queue.AddCommand(&DeleteCommand{manager: manager, name: "result.txt"})

	wg.Add(1)
	go func() {
		defer wg.Done()
		results := queue.ExecuteAll()

		for i, res := range results {
			if res.Err != nil {
				println("Command", i, "failed:", res.Err.Error())
			} else {
				println("Command", i, "succeeded")
			}
		}
	}()

	wg.Wait()
}
```

The Command pattern offers key benefits for Go developers:

* **Decoupling and Flexibility**: Separates operation invocation from actual implementation.
    
* **Undoable Operations**: Makes it straightforward to implement undo and redo functionality.
    
* **Improved Maintainability**: Centralizes request management, simplifying the addition of new operations.
    

## Chain of Responsibility

> **Chain of Responsibility** is a behavioral design pattern that lets you pass requests along a chain of handlers. Upon receiving a request, each handler decides either to process the request or to pass it to the next handler in the chain.

Imagine you're handling HTTP requests directly, explicitly performing tasks such as authentication and logging sequentially within a single function.

```go
package main

import (
	"errors"
	"fmt"
	"io"
	"net/http"
	"os"
	"time"
)


func validateAuth(r *http.Request) error {
	if r.Header.Get("Authorization") == "" {
		return errors.New("auth missing")	
	}

	return nil
}


func logReuest(r *http.Request) error {
	f, err := os.OpenFile("access.log", os.O_APPEND|os.O_CREATE|os.O_WRONLY, 0644)
	if err != nil {
		return err
	}

	defer f.Close()
	_, err = f.WriteString(r.Method + " " + r.URL.Path + "\n")
	return err
}

func handle(w http.ResponseWriter, r *http.Request) {
	if err := validateAuth(r); err != nil {
		http.Error(w, err.Error(), http.StatusUnauthorized)
		return
	}

	if err := logReuest(r); err != nil {
		http.Error(w, "logging error", http.StatusInternalServerError)
		return
	}

	io.WriteString(w, "OK")
}



func main() {
	http.HandleFunc("/", handle)

	go func(){
		if err := http.ListenAndServe(":8080", nil); err != nil {
			fmt.Println(err)
		}
	}()

	time.Sleep(time.Second)

	requestURL := fmt.Sprintf("http://localhost:%d", 8080)


	client := http.Client{}
	req , err := http.NewRequest("GET", requestURL, nil)
	if err != nil {
		panic(err)
	}

	req.Header = http.Header{
		"Authorization": {"Bearer Token"},
	}

	res , err := client.Do(req)
	if err != nil {
		fmt.Printf("error making http request: %s\n", err)
		panic(err)
	}

	fmt.Printf("client: got response!\n")
	fmt.Printf("client: status code: %d\n", res.StatusCode)

	select{}
}
```

### Problems With That Code

* **Tightly coupled logic**: All tasks are directly tied together, making it harder to modify or extend.
    
* **Poor maintainability**: Adding or removing tasks means editing the entire function.
    
* **Reduced flexibility**: Difficult to rearrange the order of tasks or insert new ones without affecting existing logic.
    

The **Chain of Responsibility** pattern decouples request-senders from receivers by allowing multiple handlers to process requests sequentially. If a handler can't process the request, it passes the request along the chain until one can.

![](https://cdn.hashnode.com/res/hashnode/image/upload/v1751376559815/08f7dbe1-c23b-41c4-a6e0-944ae056ec88.png align="center")

* `Handler` interface defines methods for handling requests (`handle(request)`) and setting the next handler (`setNext(handler)`).
    
* `BaseHandler` maintains a reference to the next handler.
    
* `ConcreteHandlers` implement specific processing logic. If unable to handle, they delegate to the next handler.
    
* `Client` sets up the chain and initiates the request handling.
    

This resolves earlier issues by:

* Providing loose coupling between handlers and request logic.
    
* Allowing easy extension or reordering of handlers.
    
* Clearly separating concerns by breaking down logic into individual handlers.
    

### Code Using the Chain of Responsibility Pattern

Implementing Chain of Responsibility involves defining a common handler interface and concrete handlers (`AuthHandler`, `LogHandler`, and `FinalHandler`) chained together.  

```go
package main

import (
	"errors"
	"fmt"
	"io"
	"net/http"
	"os"
	"time"
)

//single link
type Handler interface {

	ServeHTTP(w http.ResponseWriter, r *http.Request) error
	SetNext(h Handler)

}


type BaseHandler struct {
	next Handler
}

func (h *BaseHandler) SetNext(next Handler) {
	h.next = next	
}

func (h *BaseHandler) Next(w http.ResponseWriter, r *http.Request) error {
	if h.next != nil {
		return h.next.ServeHTTP(w, r)
	}

	return nil
}


//auth checker

type AuthHandler struct {
	BaseHandler
}

func (h *AuthHandler) ServeHTTP(w http.ResponseWriter, r *http.Request) error {
	if r.Header.Get("Authorization") == "" {
		http.Error(w, "auth missing", http.StatusUnauthorized)
		return errors.New("missing auth")
	}

	return h.Next(w,r)
}


//logger

type LogHandler struct {
	BaseHandler
	logFile string
}

func (h *LogHandler) ServeHTTP(w http.ResponseWriter, r *http.Request) error {
	f, err := os.OpenFile(h.logFile, os.O_APPEND|os.O_CREATE|os.O_WRONLY, 0644 )
	if err != nil {
		http.Error(w, "log error", http.StatusInternalServerError)
		return  err
	}

	defer f.Close()

	_, err = f.WriteString(r.Method + " " + r.URL.Path + "\n")
	if err != nil {
		http.Error(w, "log error", http.StatusInternalServerError)
		return err
	}

	return h.Next(w, r)
}


//final handler

type FinalHandler struct {
	BaseHandler
}


func (h *FinalHandler) ServeHTTP(w http.ResponseWriter, r *http.Request) error {
	io.WriteString(w, "OK")	
	return nil
}


//chaining

func chainHandler(handlers ...Handler) Handler {
	if len(handlers) == 0 {
		return nil
	}

	for i := 0; i < len(handlers) - 1; i++ {
		handlers[i].SetNext(handlers[i + 1])
	}

	return handlers[0]
}


func main() {
	auth := &AuthHandler{}
	log := &LogHandler{logFile: "access.log"}
	final := &FinalHandler{}

	handlerChain := chainHandler(auth, log, final)

	http.HandleFunc("/", func(w http.ResponseWriter, r *http.Request) {
		handlerChain.ServeHTTP(w, r)
	})

	go func() {
		if err := http.ListenAndServe(":8080", nil); err != nil{
			panic(err)
		}
	}()

	time.Sleep(time.Second)

	requestURL := fmt.Sprintf("http://localhost:%d", 8080)


	client := http.Client{}
	req , err := http.NewRequest("GET", requestURL, nil)
	if err != nil {
		panic(err)
	}

	req.Header = http.Header{
		"Authorization": {"Bearer Token"},
	}

	res , err := client.Do(req)
	if err != nil {
		fmt.Printf("error making http request: %s\n", err)
		panic(err)
	}

	fmt.Printf("client: got response!\n")
	fmt.Printf("client: status code: %d\n", res.StatusCode)

	select{}
}
```

### Goroutine-Safe Version

In scenarios with concurrent requests, ensure thread safety, particularly for shared resources (like log files). Use synchronization mechanisms (`sync.Mutex`) to prevent data races and ensure safe concurrent handling.  

```go
package main

import (
	"errors"
	"fmt"
	"io"
	"net/http"
	"os"
	"sync"
	"time"
)

//single link
type Handler interface {

	ServeHTTP(w http.ResponseWriter, r *http.Request) error
	SetNext(h Handler)

}


type BaseHandler struct {
	next Handler
}

func (h *BaseHandler) SetNext(next Handler) {
	h.next = next	
}

func (h *BaseHandler) Next(w http.ResponseWriter, r *http.Request) error {
	if h.next != nil {
		return h.next.ServeHTTP(w, r)
	}

	return nil
}


//auth checker

type AuthHandler struct {
	BaseHandler
}

func (h *AuthHandler) ServeHTTP(w http.ResponseWriter, r *http.Request) error {
	if r.Header.Get("Authorization") == "" {
		http.Error(w, "auth missing", http.StatusUnauthorized)
		return errors.New("missing auth")
	}

	return h.Next(w,r)
}


//logger

type LogHandler struct {
	BaseHandler
	logFile string
	mu sync.Mutex
}

func (h *LogHandler) ServeHTTP(w http.ResponseWriter, r *http.Request) error {
	h.mu.Lock()
	defer h.mu.Unlock()
	
	f, err := os.OpenFile(h.logFile, os.O_APPEND|os.O_CREATE|os.O_WRONLY, 0644 )
	if err != nil {
		http.Error(w, "log error", http.StatusInternalServerError)
		return  err
	}

	defer f.Close()

	_, err = f.WriteString(r.Method + " " + r.URL.Path + "\n")
	if err != nil {
		http.Error(w, "log error", http.StatusInternalServerError)
		return err
	}

	return h.Next(w, r)
}


//final handler

type FinalHandler struct {
	BaseHandler
}


func (h *FinalHandler) ServeHTTP(w http.ResponseWriter, r *http.Request) error {
	io.WriteString(w, "OK")	
	return nil
}


//chaining

func chainHandler(handlers ...Handler) Handler {
	if len(handlers) == 0 {
		return nil
	}

	for i := 0; i < len(handlers) - 1; i++ {
		handlers[i].SetNext(handlers[i + 1])
	}

	return handlers[0]
}


func main() {
	auth := &AuthHandler{}
	log := &LogHandler{logFile: "access.log"}
	final := &FinalHandler{}

	handlerChain := chainHandler(auth, log, final)

	http.HandleFunc("/", func(w http.ResponseWriter, r *http.Request) {
		handlerChain.ServeHTTP(w, r)
	})

	go func() {
		if err := http.ListenAndServe(":8080", nil); err != nil{
			panic(err)
		}
	}()

	time.Sleep(time.Second)

	requestURL := fmt.Sprintf("http://localhost:%d", 8080)


	client := http.Client{}
	req , err := http.NewRequest("GET", requestURL, nil)
	if err != nil {
		panic(err)
	}

	req.Header = http.Header{
		"Authorization": {"Bearer Token"},
	}

	res , err := client.Do(req)
	if err != nil {
		fmt.Printf("error making http request: %s\n", err)
		panic(err)
	}

	fmt.Printf("client: got response!\n")
	fmt.Printf("client: status code: %d\n", res.StatusCode)

	select{}
}
```

The Chain of Responsibility pattern provides several benefits in Go:

* **Decoupled and Flexible**: Easy to add, remove, or reorder handlers without modifying the client logic.
    
* **Improved Maintainability**: Each handler clearly focuses on one specific task.
    
* **Scalable**: Easily scales by adding new handlers as your application's complexity grows.
    

However, for very simple tasks or few handlers, this pattern might be unnecessary complexity.

## State

> **State** is a behavioral design pattern that lets an object alter its behavior when its internal state changes. It appears as if the object changed its class.

Consider you're managing a document lifecycle (`draft`, `review`, `published`, `archived`) directly using conditional logic within methods of a `Document` struct.  

```go
package main

import (
	"errors"
	"fmt"
)

type Document struct {
	Status string
}


func (d *Document) SubmitForReview() error {
	if d.Status  == "draft" {
		d.Status = "review"
		return nil
	}

	return errors.New("can only submit drafts")
}

func (d *Document) Approve() error {
	if d.Status == "review" {
		d.Status = "published"
		return nil
	}
	return errors.New("can only approve document in review")
}

func (d *Document) Archive() error {
	if d.Status == "published" {
		d.Status = "archived"
		return nil
	}
	return errors.New("can only archive published documents")
}

func (d *Document) Edit() error {
	if d.Status == "draft" || d.Status == "review" {
		return nil
	}
	return errors.New("cannot edit published or archived document")
}

func main() {
	doc := &Document{Status: "draft"}

	fmt.Println(doc.SubmitForReview()) 
	fmt.Println(doc.Approve())         
	fmt.Println(doc.Archive())        
	fmt.Println(doc.Edit())           
}
```

### Problems With That Code

* **Complex conditional logic**: State transitions handled explicitly in methods become hard to manage.
    
* **Tight coupling**: Each method directly checks and modifies the state, making it difficult to add new states.
    
* **Maintenance challenges**: Adding or changing states requires updating multiple methods, increasing the risk of errors.
    

The **State pattern** moves state-specific behaviors into separate classes (`ConcreteStates`). Each state defines behavior independently, and the object (`Context`) maintains a reference to its current state.

![](https://cdn.hashnode.com/res/hashnode/image/upload/v1751376683289/683b372e-44a4-48cf-8296-92ea0bffd632.png align="center")

* `Context` maintains a reference to the current state and delegates state-specific behaviors to it.
    
* `State` interface defines methods representing state-dependent actions.
    
* `ConcreteStates` implement these methods, managing transitions to other states.
    
* The client interacts with the context, unaware of specific state implementations.
    

This solves earlier problems by:

* Reducing complex conditional logic by encapsulating each state behavior separately.
    
* Making state transitions explicit and easily manageable.
    
* Simplifying the addition or removal of states without affecting the entire context.
    

### Code Using the State Pattern

Implementing State involves defining a `State` interface, creating concrete state structs (`DraftState`, `ReviewState`, etc.), and delegating actions through a `Document` context.

```go
package main

import (
	"errors"
	"fmt"
)



type Document struct {
	state State
}

func NewDocument() *Document {
	return &Document{state: &DraftState{}}
}


type State interface {
	SubmitForReview(*Document) error
	Approve(*Document) error
	Archive(*Document) error
	Edit(*Document) error
	Name() string 

}


func (d *Document) SubmitForReview() error {
	return d.state.SubmitForReview(d)
}


func (d *Document) Approve() error {
	return d.state.Approve(d)
}


func (d *Document) Archive() error {
	return d.state.Archive(d)
}


func (d *Document) Edit() error {
	return d.state.Edit(d)
}


func (d *Document) StateName() string {
	return d.state.Name()
}


//states


type DraftState struct{}
type ReviewState struct{}
type PublishedState struct{}
type ArchivedState struct{}



//draft receiver
func (s *DraftState) SubmitForReview(d *Document) error {
	d.state = &ReviewState{};
	return nil
}


func (s *DraftState) Approve(d *Document) error {
	return errors.New("must submit for review first")
}


func (s *DraftState) Archive(d *Document) error {
	return errors.New("cannot archive draft")
}


func (s *DraftState) Edit(d *Document) error {
	return nil
}


func (s *DraftState) Name() string {
	return "draft"
}


//review receiver

func (s *ReviewState) SubmitForReview(*Document) error { 
	return errors.New("already under review") 
}

func (s *ReviewState) Approve(d *Document) error { 
	d.state = &PublishedState{}; 
	return nil 
}


func (s *ReviewState) Archive(*Document) error { 
	return errors.New("cannot archive under review") 
}

func (s *ReviewState) Edit(*Document) error { 
	return nil 
}


func (s *ReviewState) Name() string { 
	return "review" 
}



//pubish receiver

func (s *PublishedState) SubmitForReview(*Document) error { 
	return errors.New("already published") 
}

func (s *PublishedState) Approve(*Document) error { 
	return errors.New("already published") 
}

func (s *PublishedState) Archive(d *Document) error { 
	d.state = &ArchivedState{}; 
	return nil 
}


func (s *PublishedState) Edit(*Document) error { 
	return errors.New("cannot edit published document") 
}

func (s *PublishedState) Name() string { 
	return "published" 
}



//archived recv
func (s *ArchivedState) SubmitForReview(*Document) error { 
	return errors.New("archived document") 
}


func (s *ArchivedState) Approve(*Document) error { 
	return errors.New("archived document") 
}


func (s *ArchivedState) Archive(*Document) error { 
	return errors.New("already archived") 
}

func (s *ArchivedState) Edit(*Document) error { 
	return errors.New("cannot edit archived document") 
}

func (s *ArchivedState) Name() string{ 
	return "archived"

}


func main() {
	doc := NewDocument()
	fmt.Println(doc.StateName())          // draft
	fmt.Println(doc.SubmitForReview())    
	fmt.Println(doc.StateName())          // review
	fmt.Println(doc.Approve())         
	fmt.Println(doc.StateName())          // published
	fmt.Println(doc.Archive())        
	fmt.Println(doc.StateName())          // archived
	fmt.Println(doc.Edit())               // error: cannot edit archived document
}
```

### Goroutine-Safe Version

For concurrent environments, ensure thread safety by using synchronization mechanisms (`sync.RWMutex`) when reading or modifying the state in the context.  

```go
package main

import (
	"errors"
	"fmt"
	"sync"
)



type Document struct {
	mu sync.RWMutex
	state State
}

func NewDocument() *Document {
	return &Document{state: &DraftState{}}
}


type State interface {
	SubmitForReview(*Document) error
	Approve(*Document) error
	Archive(*Document) error
	Edit(*Document) error
	Name() string 

}


func (d *Document) SubmitForReview() error {
	d.mu.Lock()
	defer d.mu.Unlock()
	return d.state.SubmitForReview(d)
}


func (d *Document) Approve() error {
	d.mu.Lock()
	defer d.mu.Unlock()
	return d.state.Approve(d)
}


func (d *Document) Archive() error {
	d.mu.Lock()
	defer d.mu.Unlock()
	return d.state.Archive(d)
}


func (d *Document) Edit() error {
	d.mu.Lock()
	defer d.mu.Unlock()
	return d.state.Edit(d)
}


func (d *Document) StateName() string {
	d.mu.Lock()
	defer d.mu.Unlock()
	return d.state.Name()
}


//states


type DraftState struct{}
type ReviewState struct{}
type PublishedState struct{}
type ArchivedState struct{}



//draft receiver
func (s *DraftState) SubmitForReview(d *Document) error {
	d.state = &ReviewState{};
	return nil
}


func (s *DraftState) Approve(d *Document) error {
	return errors.New("must submit for review first")
}


func (s *DraftState) Archive(d *Document) error {
	return errors.New("cannot archive draft")
}


func (s *DraftState) Edit(d *Document) error {
	return nil
}


func (s *DraftState) Name() string {
	return "draft"
}


//review receiver

func (s *ReviewState) SubmitForReview(*Document) error { 
	return errors.New("already under review") 
}

func (s *ReviewState) Approve(d *Document) error { 
	d.state = &PublishedState{}; 
	return nil 
}


func (s *ReviewState) Archive(*Document) error { 
	return errors.New("cannot archive under review") 
}

func (s *ReviewState) Edit(*Document) error { 
	return nil 
}


func (s *ReviewState) Name() string { 
	return "review" 
}



//pubish receiver

func (s *PublishedState) SubmitForReview(*Document) error { 
	return errors.New("already published") 
}

func (s *PublishedState) Approve(*Document) error { 
	return errors.New("already published") 
}

func (s *PublishedState) Archive(d *Document) error { 
	d.state = &ArchivedState{}; 
	return nil 
}


func (s *PublishedState) Edit(*Document) error { 
	return errors.New("cannot edit published document") 
}

func (s *PublishedState) Name() string { 
	return "published" 
}



//archived recv
func (s *ArchivedState) SubmitForReview(*Document) error { 
	return errors.New("archived document") 
}


func (s *ArchivedState) Approve(*Document) error { 
	return errors.New("archived document") 
}


func (s *ArchivedState) Archive(*Document) error { 
	return errors.New("already archived") 
}

func (s *ArchivedState) Edit(*Document) error { 
	return errors.New("cannot edit archived document") 
}

func (s *ArchivedState) Name() string{ 
	return "archived"

}


func main() {
	doc := NewDocument()
	fmt.Println(doc.StateName())          // draft
	fmt.Println(doc.SubmitForReview())   
	fmt.Println(doc.StateName())          // review
	fmt.Println(doc.Approve())        
	fmt.Println(doc.StateName())          // published
	fmt.Println(doc.Archive())            
	fmt.Println(doc.StateName())          // archived
	fmt.Println(doc.Edit())               // Error: cannot edit archived document
}
```

However, for scenarios with simple or limited states, this pattern might add unnecessary complexity.

---

# Conclusion

Design patterns are powerful tools for building better software, but in Go, not every classic pattern from OOP languages fits well with the language’s simple and practical design. In this guide, we focused only on the patterns that are truly useful and idiomatic for Go developers.

Here are some popular patterns that you might know from books or other languages, and the reasons why they are not covered in this Go guide:

**Abstract Factory**  
Not covered because Go’s interface and composition features make it easy to create related objects without needing the complex factory structure found in languages like Java or C++.

**Facade**  
Go’s preference for flat, small packages and simple APIs means that a facade layer is rarely needed. Most Go projects expose a clear and minimal API directly from packages.

**Flyweight**  
Go’s memory management and garbage collector already optimise for efficient object use in most situations. The pattern is not common or necessary in typical Go applications.

**Bridge**  
Go’s interface system and preference for composition already solve the problems Bridge addresses, in a much simpler way, without requiring the pattern’s structure.

**Template Method**  
This pattern relies on inheritance and overriding methods, which are not available in Go. Go encourages composition and interfaces instead of class hierarchies.

**Memento**  
Saving and restoring object state can be done easily using structs and simple functions in Go. The pattern’s class-based structure is unnecessary in most Go cases.

**Visitor**  
Visitor depends on double-dispatch and deep type hierarchies, which do not fit naturally with Go’s flat and interface-based approach. Using interfaces and type switches is usually enough for similar use-cases.

**Mediator**  
Go’s channels and goroutines already provide simple and powerful ways for components to communicate, often making an explicit Mediator pattern unnecessary.

**Iterator**  
Go’s built-in `range` works naturally for most collection types, so a dedicated iterator pattern is rarely needed.

If you are interested in any of these patterns or have a use-case where you think they might be needed in Go, feel free to ask or share your thoughts! At the end of the day, the best pattern is the one that keeps your code simple, clear, and easy to maintain.

> Thanks for reading, and happy Go coding!