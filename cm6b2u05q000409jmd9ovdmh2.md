---
title: "Understanding Linux Cron for Task Scheduling (with Golang Example)"
seoTitle: "Mastering Cron in Linux: Comprehensive Guide with Golang Integration"
seoDescription: "Learn how to automate tasks in Linux using cron and crontab. Understand the internal workings of the cron daemon, schedule jobs efficiently, and explore Gol"
datePublished: Fri Jan 24 2025 18:09:51 GMT+0000 (Coordinated Universal Time)
cuid: cm6b2u05q000409jmd9ovdmh2
slug: mastering-linux-cron-guide-golang-integration
cover: https://cdn.hashnode.com/res/hashnode/image/upload/v1737741776993/30299b11-f1fb-4eac-8cce-2c50d6732586.png
tags: linux, go, system-architecture, scripting, cronjob, task-management

---

Cron is a built-in utility on Linux and Unix-like systems. Its main purpose is to schedule and automate tasks (known as jobs) so that you do not have to run them manually. These automated tasks can include sending emails, cleaning up files, monitoring websites, and much more.

In this blog, we will explore how Cron works behind the scenes, how to set up tasks in Linux, and then see how to replicate a similar scheduling mechanism using Golang’s popular Cron package.

# Crontab File Basics

The word “crontab” comes from “cron table.” A **crontab** file is where you define your scheduled tasks (cron jobs). Each user on your system can have a separate crontab file. To create or edit a crontab file, you use:

```bash
crontab -e
```

This opens a text editor where you can add or modify cron jobs. Each line in a crontab file represents a schedule (time pattern) followed by the command to execute.

# Star Notation in Crontab

A typical crontab entry follows this format:

```bash
*  *  *  *  *  command
```

Each asterisk (`*`) represents a time field, in this order:

1. **Minute** (0–59)
    
2. **Hour** (0–23)
    
3. **Day of Month** (1–31)
    
4. **Month** (1–12)
    
5. **Day of Week** (0–7) (both 0 and 7 represent Sunday)
    

The `*` in any field means “every possible value.” For example, putting `*` in the “minute” field means every minute, while putting `*/5` in the “minute” field means “every 5 minutes.”

# How Cron Daemon Works Internally

## Spool Directories and Crontab Files

When you schedule tasks, Cron stores your crontab file in special spool directories, commonly found under:

```bash
/var/spool/cron
```

for user-specific crontab files. System-wide schedules also exist in:

```bash
/etc/crontab
/etc/cron.*
```

These can be used by administrators for system-level tasks.

## Cron Daemon’s Process Cycle

1. **Startup**: Cron starts automatically when the system boots.
    
2. **Reading Crontabs**: It loads the crontab files from the spool directories.
    
3. **Minute-by-Minute Check**: Every minute, Cron checks the current time against all the schedules in every crontab.
    
4. **Task Execution**: When the current time matches a time pattern in a crontab entry, Cron launches that task as a child process. This ensures the task has its own environment and does not interfere with the Cron daemon itself.
    

## Environment Variables

Cron jobs typically run with a restricted environment. By default, Cron uses the environment variables from:

```javascript
/etc/environment
```

and some minimal defaults. If your job needs a specific environment (like a custom `PATH` or other variables), you have to set them inside your script or add them at the top of your crontab file.

# What Are Linux Tasks?

In Linux, a “task” or a “job” can be any script, program, or command. Common examples include:

* Database backups
    
* Log file rotation
    
* Sending email notifications
    
* Monitoring or health checks
    
* Cleaning temporary files
    

With Cron, you can specify exactly when to run these tasks, making it a powerful tool for time-based automation.

# Simple Cron Script to Monitor Google.com Every 5 Minutes

Let us create a simple shell script that checks if [google.com](https://google.com/) is reachable. We will schedule it to run every 5 minutes.

1. **Create the Bash Script**
    
    ```bash
    #!/bin/bash
    if ping -c 1 google.com &> /dev/null
    then
        echo "$(date): google.com is reachable."
    else
        echo "$(date): google.com is not reachable."
    fi
    ```
    
    * Save this as `check_google.sh`.
        
    * Make it executable:
        
        ```bash
        chmod +x check_google.sh
        ```
        
2. **Set Up a Cron Job**
    
    To schedule it every 5 minutes:
    
    ```bash
    crontab -e
    ```
    
    Then add a line like this to your crontab:
    
    ```bash
    */5 * * * * ./check_google.sh >> ./check_google.log 2>&1
    ```
    
    * `*/5` in the minutes field means “run every 5 minutes.”
        
    * We append both standard output and error to `check_google.log`.
        

# Scheduling Tasks in Golang with Cron Package

Cron is not limited to shell scripts. We can use Golang’s **Cron package** (commonly known as `github.com/robfig/cron/v3`) to create scheduled tasks in our Go applications.

### Installing the Cron Package

1. Create a new folder and initialize a Go module:
    
    ```bash
    mkdir go-cron-check
    cd go-cron-check
    go mod init example.com/go-cron-check
    ```
    
2. Install the package:
    
    ```bash
    go get github.com/robfig/cron/v3
    ```
    

### Writing the Go Code

Create a file called `main.go`:

```go
package main

import (
    "fmt"
    "net/http"
    "time"

    "github.com/robfig/cron/v3"
)

func main() {
    c := cron.New()

    // Schedule a job to run every 5 minutes (*/5 in cron terms)
    c.AddFunc("*/5 * * * *", func() {
        checkGoogle()
    })

    // Start the cron scheduler
    c.Start()

    // Keep the main goroutine alive
    select {}
}

func checkGoogle() {
    client := &http.Client{
        Timeout: 5 * time.Second,
    }

    resp, err := client.Get("https://www.google.com")
    if err != nil {
        fmt.Println(time.Now().Format(time.RFC3339), ": google.com is not reachable. Error:", err)
        return
    }
    defer resp.Body.Close()

    if resp.StatusCode == 200 {
        fmt.Println(time.Now().Format(time.RFC3339), ": google.com is reachable.")
    } else {
        fmt.Println(time.Now().Format(time.RFC3339), ": google.com returned status:", resp.StatusCode)
    }
}
```

* We initialize a new `cron` scheduler.
    
* We add a function that runs at the “\*/5 \* \* \* \*” schedule, which corresponds to every 5 minutes.
    
* The `checkGoogle` function checks if `google.com` returns HTTP status code 200 and prints the result.
    

### Running the Go Program in Background

You can run your Go application in two ways:

1. **Directly with** `go run`:
    
    ```bash
    go run main.go >> go-cron-check.log 2>&1 &
    ```
    
    * `>> go-cron-check.log` appends standard output to `go-cron-check.log`.
        
    * `2>&1` redirects standard error to the same log file.
        
    * `&` at the end runs it in the background.
        
2. **Build the Go binary and run it:**
    
    ```bash
    go build -o go-cron-check
    ./go-cron-check >> go-cron-check.log 2>&1 &
    ```
    

Either way, the logs will be saved in `go-cron-check.log`.

## Deeper Look: Comparing Linux Cron vs. Go’s Cron

| Aspect | Linux Cron | Go’s Cron Package |
| --- | --- | --- |
| **Setup** | Edit crontab files under `/var/spool/cron` or `/etc/crontab` | Add functions in Go code using `cron.New()` |
| **Time Format** | 5-field Cron expression (`* * * * *`) | Similar 5-field format (`"*/5 * * * *"`) |
| **Environment** | Minimal environment; usually no user-specific shells | Inherits environment from the running Go process |
| **Security** | Requires system or user-level privileges for editing crontabs | Controlled by how you run the Go process |
| **Logging** | You can direct output to any log file manually in crontab | Handle logs inside Go or redirect from the command line |
| **Maintenance** | Cron runs as a system daemon; each user manages separate crontab | The Go program itself must keep running to maintain schedule |

Each approach has its advantages. For simple system tasks, Linux Cron is often enough. For more complex logic within an application, Go’s Cron package provides greater control and flexibility.

## Conclusion

Cron is at the heart of automated task scheduling on Linux systems. It works by reading crontab files from the spool directory and matches them against the current time, spawning new processes for each job. This mechanism allows you to automate a variety of tasks efficiently.

While Linux Cron is powerful for system-wide scheduling, you can also embed scheduling functionality right into your applications using Go’s Cron package. This allows you to create self-contained programs that run scheduled tasks without relying on external crontab files.

Whether you decide to use Linux Cron or Go’s Cron package, you now have a thorough understanding of how cron jobs are scheduled and executed. You can combine these approaches — or choose the one that best fits your workflow — to keep your systems and applications running smoothly and automatically.