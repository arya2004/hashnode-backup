---
title: "Forward Mode Automatic Differentiation in Go: A Practical Guide with Dual Numbers"
seoTitle: "Forward Mode Automatic Differentiation in Golang: Dual Numbers & Code "
seoDescription: "Learn the math behind it and get fully functional Go code for differentiating polynomial and advanced functions."
datePublished: Sun Mar 02 2025 14:11:51 GMT+0000 (Coordinated Universal Time)
cuid: cm7rpmgmp000009lb53m25t8y
slug: forward-mode-automatic-differentiation-go-dual-numbers
cover: https://cdn.hashnode.com/res/hashnode/image/upload/v1740924510903/c64ab212-80a1-43e0-93ab-c222485dd24b.png
tags: go, machine-learning, mathematics

---

Differentiation is at the heart of calculus, telling us the slope of a function at any given point. This idea finds applications in physics, machine learning, graphics, and engineering. In this blog, we explore **Forward Mode Automatic Differentiation (AD)**—a technique that is both fast and exact. We’ll cover the underlying mathematics using dual numbers, work through both a simple and an advanced example, and provide complete Go implementations. Finally, we’ll mention some popular libraries that use AD internally.

## Traditional Differentiation Approaches

Before diving into forward mode AD, let’s quickly review two common methods for computing derivatives:

* **Symbolic Differentiation:**  
    Here, you apply a set of known rules (e.g., the power rule: \\(\frac{d}{dx} \left( x^n \right) = n x^{n-1}\\) ) to a symbolic expression. This method is exact but becomes slow and rigid for complex functions.
    
* **Numerical Differentiation:**  
    This approximates the derivative by evaluating the function at two close points:
    

$$f'(x) \approx \frac{f(x+h) - f(x)}{h}$$

It is fast and flexible but suffers from approximation errors when \\(h\\) is very small.

## The Magic of Forward Mode AD and Dual Numbers

Forward mode AD offers the best of both worlds—it is as fast as numerical methods and as exact as symbolic ones. Its secret is the use of **dual numbers**.

### Dual Numbers Explained

A dual number is of the form:

$$a + b\varepsilon$$

where:

* \\(a\\) is the **real part**,
    
* \\(b\\) is the **dual part**,
    
* \\(\varepsilon \\) is a special number with the property \\(\varepsilon^2 = 0\\) (but \\(\varepsilon \neq 0\\)).
    

When you evaluate a function \\(f(x) \\) at \\(x + \varepsilon\\), it expands as:

$$f(x+\varepsilon) = f(x) + f'(x)\varepsilon$$

The coefficient of \\(\varepsilon \\) immediately gives you the derivative \\(f'(x)\\) with just one function evaluation.

### Dual Number Representation in Go

Below is the Go code snippet that defines a dual number and its basic operations:

```go
// Dual represents a dual number: a + bε, where ε² = 0.
type Dual struct {
	Real float64 // The real part 'a'
	Dual float64 // The dual part 'b'
}

// Add returns the sum of two dual numbers.
func (d Dual) Add(other Dual) Dual {
	return Dual{
		Real: d.Real + other.Real,
		Dual: d.Dual + other.Dual,
	}
}

// Mul returns the product of two dual numbers.
// (a + bε) * (c + dε) = ac + (ad + bc)ε, since ε² = 0.
func (d Dual) Mul(other Dual) Dual {
	return Dual{
		Real: d.Real * other.Real,
		Dual: d.Real*other.Dual + d.Dual*other.Real,
	}
}
```

This snippet forms the core of our implementation. Now let’s see how the substitution process works in two examples.

## Example 1: Simple Polynomial

Let’s differentiate:

$$f(x) = x^2 + 3x + 5$$

**Mathematical Expansion:**  
Substitute \\(x\\) with \\(x + \varepsilon\\):

$$\begin{aligned} f(x+\varepsilon) &= (x+\varepsilon)^2 + 3(x+\varepsilon) + 5 \\ &= x^2 + 2x\varepsilon + \varepsilon^2 + 3x + 3\varepsilon + 5 \\ &= (x^2 + 3x + 5) + (2x+3)\varepsilon \quad (\text{since } \varepsilon^2=0) \end{aligned}$$

Thus, \\(f'(x) = 2x + 3\\).

### Go Implementation for the Simple Example

```go
package main

import (
	"fmt"
)

// Dual represents a dual number: a + bε, where ε² = 0.
type Dual struct {
	Real float64
	Dual float64
}

// Add returns the sum of two dual numbers.
func (d Dual) Add(other Dual) Dual {
	return Dual{Real: d.Real + other.Real, Dual: d.Dual + other.Dual}
}

// Mul returns the product of two dual numbers.
func (d Dual) Mul(other Dual) Dual {
	return Dual{
		Real: d.Real * other.Real,
		Dual: d.Real*other.Dual + d.Dual*other.Real,
	}
}

// Pow returns the dual number raised to an integer power.
func (d Dual) Pow(n int) Dual {
	result := Dual{Real: 1, Dual: 0}
	for i := 0; i < n; i++ {
		result = result.Mul(d)
	}
	return result
}

// f defines the function: f(x) = x² + 3x + 5.
func f(x Dual) Dual {
	return x.Pow(2).Add(Dual{Real: 3, Dual: 0}.Mul(x)).Add(Dual{Real: 5, Dual: 0})
}

// differentiate computes the derivative of f at x0.
func differentiate(f func(Dual) Dual, x0 float64) float64 {
	x := Dual{Real: x0, Dual: 1}
	return f(x).Dual
}

func main() {
	x0 := 2.0
	value := f(Dual{Real: x0, Dual: 0}).Real
	deriv := differentiate(f, x0)
	fmt.Printf("Simple Example: At x = %v, f(x) = %v and f'(x) = %v\n", x0, value, deriv)
}
```

## Example 2: Advanced Trigonometric-Exponential Function

Now, consider a more advanced function:

$$g(x) = \sin(x) \times e^x$$

Using the product rule, its derivative is:

$$g'(x) = e^x (\sin(x) + \cos(x))$$

### Extending Dual Numbers for Transcendental Functions

We define the sine and exponential for dual numbers using Taylor series expansion:

* **Sine:** \\(\sin(a + b\varepsilon) = \sin(a) + b\cos(a)\varepsilon\\)
    
* **Exponential:** \\(e^{(a + b\varepsilon)} = e^a + b\,e^a\varepsilon\\)
    

### Go Implementation for the Advanced Example

```go
package main

import (
	"fmt"
	"math"
)

// Dual represents a dual number: a + bε.
type Dual struct {
	Real float64
	Dual float64
}

// Add adds two dual numbers.
func (d Dual) Add(other Dual) Dual {
	return Dual{Real: d.Real + other.Real, Dual: d.Dual + other.Dual}
}

// Mul multiplies two dual numbers.
func (d Dual) Mul(other Dual) Dual {
	return Dual{
		Real: d.Real * other.Real,
		Dual: d.Real*other.Dual + d.Dual*other.Real,
	}
}

// Sin computes the sine of a dual number.
func (d Dual) Sin() Dual {
	return Dual{
		Real: math.Sin(d.Real),
		Dual: d.Dual * math.Cos(d.Real),
	}
}

// Exp computes the exponential of a dual number.
func (d Dual) Exp() Dual {
	val := math.Exp(d.Real)
	return Dual{
		Real: val,
		Dual: d.Dual * val,
	}
}

// g defines the function: g(x) = sin(x) * exp(x).
func g(x Dual) Dual {
	return x.Sin().Mul(x.Exp())
}

// differentiate computes the derivative of function f at x0.
func differentiate(f func(Dual) Dual, x0 float64) float64 {
	x := Dual{Real: x0, Dual: 1}
	return f(x).Dual
}

func main() {
	x0 := 1.0
	value := g(Dual{Real: x0, Dual: 0}).Real
	deriv := differentiate(g, x0)
	fmt.Printf("Advanced Example: At x = %v, g(x) = %v and g'(x) = %v\n", x0, value, deriv)

	// Expected derivative: e^x (sin(x) + cos(x)) at x = 1
	expected := math.Exp(1) * (math.Sin(1) + math.Cos(1))
	fmt.Printf("Expected derivative: %v\n", expected)
}
```

## Where Is Forward Mode AD Used?

Forward mode AD is not just an academic exercise—it’s employed in many real-world libraries and applications:

* **Machine Learning:**  
    While frameworks like TensorFlow and PyTorch typically use reverse mode AD (backpropagation) for training, forward mode AD is used for tasks like Jacobian-vector products and directional derivatives.
    
* **Scientific Computing:**  
    Libraries such as [Autograd](https://github.com/HIPS/autograd), [JAX](https://github.com/google/jax), and C++ tools like [Ceres Solver](http://ceres-solver.org/) leverage AD for efficient and accurate derivative computations.
    
* **Graphics and Robotics:**  
    AD is also used in computer graphics, robotics, and control systems for real-time sensitivity analysis and optimization.
    

## Conclusion

Forward Mode Automatic Differentiation using dual numbers provides an elegant and efficient way to compute derivatives accurately. By extending our number system with dual numbers, we can propagate derivative information through any function with a single evaluation. This blog demonstrated both a simple polynomial example and a more advanced trigonometric-exponential example, along with full Go implementations.

Whether you are developing machine learning models or performing scientific computations, forward mode AD offers a robust tool to compute derivatives seamlessly.

Happy coding and happy differentiating!