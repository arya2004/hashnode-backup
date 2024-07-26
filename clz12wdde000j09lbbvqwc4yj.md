---
title: "Understanding Database Isolation Levels with MySQL and PostgreSQL"
seoTitle: "Database Isolation Levels with MySQL and PostgreSQL"
datePublished: Thu Jul 25 2024 09:36:03 GMT+0000 (Coordinated Universal Time)
cuid: clz12wdde000j09lbbvqwc4yj
slug: understanding-database-isolation-levels-with-mysql-and-postgresql
cover: https://cdn.hashnode.com/res/hashnode/image/upload/v1721768870756/dc14665e-8bc5-49ed-8d20-691520034dd0.png
tags: postgresql, mysql, databases, sql

---

When working with database transactions, one crucial decision we must make is choosing the appropriate isolation level for our application. Although there’s a well-defined standard, each database engine might choose to implement it differently, leading to variations in behavior at each isolation level. In this blog, we will explore in-depth how each isolation level works in MySQL and PostgreSQL by running concrete SQL queries.

# The Theory Behind Isolation Levels

A database transaction must satisfy the ACID properties: Atomicity, Consistency, Isolation, and Durability. Isolation is one of the critical properties, ensuring that all concurrent transactions do not affect each other at the highest level. However, transactions can interfere with each other in several ways, leading to various "read phenomena."

## Read Phenomena

1. **Dirty Read:** Occurs when a transaction reads data written by another concurrent transaction that has not been committed yet. This can lead to using incorrect data if the other transaction is rolled back.
    
2. **Non-repeatable Read:** Happens when a transaction reads the same record twice and sees different values because the row has been modified by another transaction committed after the first read.
    
3. **Phantom Read:** Similar to non-repeatable read but affects queries searching for multiple rows. The same query returns a different set of rows due to changes made by other recently committed transactions.
    
4. **Serialization Anomaly:** Occurs when the result of a group of concurrent committed transactions cannot be achieved if they are run sequentially without overlapping.
    

## ANSI Standard Isolation Levels

To deal with these phenomena, ANSI defined four standard isolation levels:

1. **Read Uncommitted:** The lowest isolation level where transactions can see data written by other uncommitted transactions, allowing dirty reads.
    
2. **Read Committed:** Transactions can only see data that has been committed by other transactions, preventing dirty reads.
    
3. **Repeatable Read:** Ensures that the same select query always returns the same result, even if other concurrent transactions have committed changes.
    
4. **Serializable:** The highest isolation level, guaranteeing that concurrent transactions yield the same result as if they were executed sequentially without overlapping.
    

# Practical Implementation in MySQL and PostgreSQL

Let's run some transactions with different levels of isolation in MySQL and PostgreSQL to see how they handle the various read phenomena. We have two running Docker containers: one with PostgreSQL version 12 and the other with MySQL version 8, both containing a simple bank database schema with initial data.

## Read Uncommitted in MySQL

### **Connecting to MySQL and Accessing the Database**

Let's begin by connecting to the MySQL console and accessing the database:

```sql
mysql -u username -p
USE your_database;
```

### Checking and Setting Transaction Isolation Levels

To check the transaction isolation level of the current session, you can run the following query:

```sql
SELECT @@transaction_isolation;
```

![](https://cdn.hashnode.com/res/hashnode/image/upload/v1721898430907/f1d6b3a4-b90a-4116-979f-3ec3fa885bf6.png align="center")

By default, MySQL uses the `REPEATABLE READ` isolation level. This level is only applied to the specific MySQL console session. There is also a global isolation level that applies to all sessions when they first start. To get its value, you can run:

```sql
SELECT @@global.transaction_isolation;
```

![](https://cdn.hashnode.com/res/hashnode/image/upload/v1721898456033/c34c586d-6bda-4001-8fca-7760a92f23ba.png align="center")

To change the isolation level of the current session, use the following query:

```sql
SET SESSION TRANSACTION ISOLATION LEVEL [LEVEL_NAME];
```

For example, to set the isolation level to `READ UNCOMMITTED`, run:

```sql
SET SESSION TRANSACTION ISOLATION LEVEL READ UNCOMMITTED;
```

![](https://cdn.hashnode.com/res/hashnode/image/upload/v1721898473805/548f30b5-3fe7-4a33-bc7a-72bfdcba99a4.png align="center")

To verify the change, you can run the select query again:

```sql
SELECT @@transaction_isolation;
```

Note that this change will only affect all future transactions of the current session, not those running in another session of the MySQL console.

### Demonstrating Transaction Isolation Levels

To demonstrate the effects of different isolation levels, we will simulate interference between two concurrent transactions.

1. **Open Two MySQL Console Sessions**:
    
    Open two terminal windows side by side and start a new MySQL console in each:
    
    ```bash
    mysql -u username -p
    USE your_database;
    ```
    
2. **Set Isolation Levels**:
    
    Set the isolation level of both sessions to `READ UNCOMMITTED`:
    
    ```sql
    SET SESSION TRANSACTION ISOLATION LEVEL READ UNCOMMITTED;
    ```
    
3. **Start Transactions**:
    
    Start a new transaction in each session:
    
    ```sql
    START TRANSACTION;
    ```
    
    Alternatively, you can use:
    
    ```sql
    BEGIN;
    ```
    
4. **Perform Operations**:
    
    In the first session (Transaction 1), run a simple select query:
    
    ```sql
    SELECT * FROM accounts;
    ```
    
    ![](https://cdn.hashnode.com/res/hashnode/image/upload/v1721898611918/d935beb3-5e4a-470e-9525-687bd3fc9232.png align="center")
    
    Assume there are three accounts with a balance of $100 each. In the second session (Transaction 2), select the first account:
    
    ```sql
    SELECT * FROM accounts WHERE id = 1;
    ```
    
    ![](https://cdn.hashnode.com/res/hashnode/image/upload/v1721898615305/377757ea-aa39-434a-aa11-accac19260c9.png align="center")
    
    You'll see the account with a $100 balance. Now, in Transaction 1, update the balance of the first account:
    
    ```sql
    UPDATE accounts SET balance = balance - 10 WHERE id = 1;
    ```
    
    Verify the change:
    
    ```sql
    SELECT * FROM accounts WHERE id = 1;
    ```
    
    ![](https://cdn.hashnode.com/res/hashnode/image/upload/v1721898637624/2a2868f6-5c35-4658-910e-c4c403b1686e.png align="center")
    
    The balance should now be $90. Without committing Transaction 1, run the same select query in Transaction 2:
    
    ```sql
    SELECT * FROM accounts WHERE id = 1;
    ```
    
    ![](https://cdn.hashnode.com/res/hashnode/image/upload/v1721898660014/644b0c91-d5d0-4d16-b040-ca52485f3b62.png align="center")
    
    Despite not being committed, Transaction 2 sees the modified value of $90. This phenomenon is known as a **dirty read**, and it occurs because we are using the `READ UNCOMMITTED` isolation level.
    
5. **Commit Transactions**:
    
    Finally, commit both transactions:
    
    ```sql
    COMMIT;
    ```
    

## Read Uncommitted in **PostgreSQL**

### Default Isolation Levels: PostgreSQL vs. MySQL

In MySQL, the default isolation level is **Repeatable Read**, which ensures that if a row is read twice in the same transaction, the values will be the same. PostgreSQL's default isolation level is **Read Committed**, which provides a slightly lower level of isolation.

### Setting Up PostgreSQL Consoles

To explore these concepts in PostgreSQL, we'll use two terminal windows to simulate concurrent transactions. Open two PostgreSQL consoles by running:

```bash
psql -U your_username -d your_database
```

### Checking the Current Isolation Level

To check the current isolation level in PostgreSQL, use the following command:

```sql
SHOW transaction_isolation;
```

![](https://cdn.hashnode.com/res/hashnode/image/upload/v1721899392174/e7fdf446-f44c-4535-a991-31112854644e.png align="center")

By default, this will return `read committed`.

### Changing the Isolation Level

In MySQL, we set the session isolation level before starting transactions. However, in PostgreSQL, we set the isolation level within the transaction. This setting only affects that specific transaction.

### Practical Example: Read Uncommitted

Let's start two transactions in separate console windows.

**Console 1:**

```sql
BEGIN;
SET TRANSACTION ISOLATION LEVEL READ UNCOMMITTED;
SHOW transaction_isolation;
```

![](https://cdn.hashnode.com/res/hashnode/image/upload/v1721899431175/ad0f213d-7c41-45a8-bbb2-14c0aff049e3.png align="center")

This will show that the isolation level is now `read uncommitted`.

**Console 2:**

```sql
BEGIN;
SET TRANSACTION ISOLATION LEVEL READ UNCOMMITTED;
SHOW transaction_isolation;
```

Both transactions are now set to `read uncommitted`.

### Testing Read Uncommitted

Let's see the behavior of `read uncommitted` in PostgreSQL.

**Console 1:**

```sql
SELECT * FROM accounts;
```

![](https://cdn.hashnode.com/res/hashnode/image/upload/v1721899537273/f343ed5d-531d-4033-9638-09883b640056.png align="center")

Suppose this returns three accounts with a balance of 100 dollars each.

**Console 2:**

```sql
SELECT * FROM accounts WHERE id = 1;
```

![](https://cdn.hashnode.com/res/hashnode/image/upload/v1721899540242/d220ee52-e499-402b-b71d-dda784dee6aa.png align="center")

This selects the account with ID 1.

**Console 1:**

```sql
UPDATE accounts SET balance = 90 WHERE id = 1;
```

![](https://cdn.hashnode.com/res/hashnode/image/upload/v1721899545021/c4cdba3d-ba9c-49d2-9d2b-ec4f47f6b6b2.png align="center")

The balance of account 1 is now updated to 90 dollars.

**Console 2:**

```sql
SELECT * FROM accounts WHERE id = 1;
```

![](https://cdn.hashnode.com/res/hashnode/image/upload/v1721899571505/fc39fd14-b2e7-4206-8678-3265384bf2bd.png align="center")

Surprisingly, this still shows the balance as 100 dollars, even though the isolation level is `read uncommitted`.

### Understanding the Behavior

This unexpected behavior occurs because PostgreSQL treats `read uncommitted` the same as `read committed`. According to PostgreSQL documentation, `read uncommitted` behaves identically to `read committed`. Essentially, PostgreSQL only supports three isolation levels, with `read committed` being the lowest.

### Committing Transactions

**Console 1:**

```sql
COMMIT;
```

**Console 2:**

```sql
SELECT * FROM accounts WHERE id = 1;
```

After committing the transaction in Console 1, the balance of account 1 is now correctly shown as 90 dollars in Console 2..

## Read Committed in MySQL

### Setting Up Read Committed Isolation Level

To understand how Read Committed works, let's set up an example. We'll start by setting the isolation level to Read Committed and observing its behavior in a multi-transaction scenario.

```sql
-- Set the session isolation level to Read Committed
SET SESSION TRANSACTION ISOLATION LEVEL READ COMMITTED;
```

Let's verify the isolation level:

```sql
-- Check the current isolation level
SELECT @@transaction_isolation;
```

\-- Transaction 2 is blocked until Transaction 1 commits

Now, we start a new transaction:

```sql
-- Begin a new transaction
BEGIN;
```

In another session, we do the same:

```sql
-- Set the session isolation level to Read Committed
SET SESSION TRANSACTION ISOLATION LEVEL READ COMMITTED;

-- Check the current isolation level
SHOW TRANSACTION ISOLATION LEVEL;

-- Begin a new transaction
BEGIN;
```

### Initial State of the Accounts Table

Assume our `accounts` table has the following state:

```sql
SELECT * FROM accounts;
```

![](https://cdn.hashnode.com/res/hashnode/image/upload/v1721898778997/e4695031-d576-40a7-ae78-9e72bea591fa.png align="center")

### Preventing Dirty Reads

In transaction 2, we select account with ID 1:

```sql
-- Transaction 2
SELECT * FROM accounts WHERE id = 1;
```

In transaction 1, we update the balance of account 1:

```sql
-- Transaction 1
UPDATE accounts SET balance = balance - 10 WHERE id = 1;
```

The change is not visible in transaction 2 because the update has not been committed:

```sql
-- Transaction 2
SELECT * FROM accounts WHERE id = 1;
```

![](https://cdn.hashnode.com/res/hashnode/image/upload/v1721898877865/032d4ff6-d145-4eb1-97df-b9fb3862c111.png align="center")

This demonstrates that the Read Committed isolation level prevents dirty reads. The update in transaction 1 is not visible to transaction 2 until it is committed.

### Non-Repeatable Reads

Next, let's see how Read Committed handles non-repeatable reads. In transaction 2, we select accounts with a balance greater than or equal to 90 dollars:

```sql
-- Transaction 2
SELECT * FROM accounts WHERE balance >= 90;
```

We commit transaction 1:

```sql
-- Transaction 1
COMMIT;
```

![](https://cdn.hashnode.com/res/hashnode/image/upload/v1721898904628/56078422-2dc0-4371-bb84-f29136935865.png align="center")

Now, if we re-select account 1 in transaction 2, the balance has changed:

```sql
-- Transaction 2
SELECT * FROM accounts WHERE id = 1;
```

![](https://cdn.hashnode.com/res/hashnode/image/upload/v1721898932839/a270f3b8-1b97-4912-ad28-9673fd60c2bb.png align="center")

This is a non-repeatable read phenomenon because the same query within the same transaction returns different results before and after another transaction commits.

### Phantom Reads

To illustrate phantom reads, let's re-run the query to get all accounts with a balance of at least 80 dollars:

```sql
-- Transaction 2
SELECT * FROM accounts WHERE balance >= 80;
```

Initially, this query returned three rows, but after committing transaction 1, it only returns two. This change is due to a committed transaction in another session, leading to the phantom read phenomenon.

The Read Committed isolation level provides a balance between consistency and performance. It prevents dirty reads by ensuring that a transaction only sees committed changes from other transactions. However, it does allow non-repeatable reads and phantom reads, which can lead to inconsistencies in certain scenarios.

## Read Committed in **PostgreSQL**

The Read Committed isolation level ensures that a transaction can only see changes committed by other transactions. Let's demonstrate this with two concurrent transactions.

```sql
-- Transaction 1
BEGIN;
SET TRANSACTION ISOLATION LEVEL READ COMMITTED;
SHOW TRANSACTION ISOLATION LEVEL;
```

```sql
-- Transaction 2
BEGIN;
SET TRANSACTION ISOLATION LEVEL READ COMMITTED;
SHOW TRANSACTION ISOLATION LEVEL;
```

![](https://cdn.hashnode.com/res/hashnode/image/upload/v1721899645833/9d17b18f-cc46-4990-8571-7661f7da0ac8.png align="center")

### Checking for Dirty Reads

First, we check if dirty reads are possible by performing a select operation in both transactions.

```sql
-- Transaction 1
SELECT * FROM accounts;

-- Transaction 2
SELECT * FROM accounts WHERE id = 1;
```

![](https://cdn.hashnode.com/res/hashnode/image/upload/v1721899654350/21da6f6f-0cca-4afb-85d7-ed383ca2fa26.png align="center")

Now, let's modify the balance in Transaction 1 but do not commit it yet.

```sql
-- Transaction 1
UPDATE accounts SET balance = balance - 10 WHERE id = 1;
```

![](https://cdn.hashnode.com/res/hashnode/image/upload/v1721899673090/b2d57b2d-14b1-4d25-a782-f516c4f54bd4.png align="center")

If we check the balance of account 1 in Transaction 2, it will still show the old balance because Transaction 1 has not committed its changes.

```sql
-- Transaction 2
SELECT * FROM accounts WHERE id = 1;
```

### Committing Changes and Phantom Reads

Once we commit Transaction 1, Transaction 2 can see the updated balance.

```sql
-- Transaction 1
COMMIT;
```

![](https://cdn.hashnode.com/res/hashnode/image/upload/v1721899717302/2bee1c93-f3d3-4857-b277-ee40285284a8.png align="center")

```sql
-- Transaction 2
SELECT * FROM accounts WHERE id = 1;
```

![](https://cdn.hashnode.com/res/hashnode/image/upload/v1721899724204/637f3052-7f32-43df-98d9-91cc08fa2fb4.png align="center")

If we update the balance in Transaction 1 and commit it, the search results in Transaction 2 will change, indicating a phantom read.

```sql
-- Transaction 1
BEGIN;
UPDATE accounts SET balance = 70 WHERE id = 1;
COMMIT;
```

## Repeatable Read in MySQL

Let's start by setting the transaction isolation level to `REPEATABLE READ` and examining its behavior through a series of steps and code examples.

```sql
-- Set the session's transaction isolation level to REPEATABLE READ
SET SESSION TRANSACTION ISOLATION LEVEL REPEATABLE READ;

-- Verify the isolation level
SHOW VARIABLES LIKE 'transaction_isolation';
```

![](https://cdn.hashnode.com/res/hashnode/image/upload/v1721898991419/a395fb4c-f9cb-441f-a746-17497860dfe3.png align="center")

### Starting Concurrent Transactions

We'll begin two separate transactions and perform operations to observe the behavior under `REPEATABLE READ`.

```sql
-- Start transaction 1
START TRANSACTION;

-- Select all accounts in transaction 1
SELECT * FROM accounts;

-- Start transaction 2 in a new session
START TRANSACTION;

-- Select account with ID 1 in transaction 2
SELECT * FROM accounts WHERE id = 1;

-- Select accounts with a balance of at least 80 dollars
SELECT * FROM accounts WHERE balance >= 80;
```

### Modifying Data in Transaction 1

Next, we'll modify the balance of account 1 in transaction 1 and observe the changes.

```sql
-- In transaction 1, subtract 10 from the balance of account 1
UPDATE accounts SET balance = balance - 10 WHERE id = 1;

-- Select all accounts to see the current state in transaction 1
SELECT * FROM accounts;

-- Commit transaction 1
COMMIT;
```

![](https://cdn.hashnode.com/res/hashnode/image/upload/v1721899067382/de78d4f1-f174-442e-a1e9-4acc86db7c02.png align="center")

### Reading Data in Transaction 2

Let's check if transaction 2 can see the changes made by transaction 1.

```sql
-- Select account with ID 1 in transaction 2
SELECT * FROM accounts WHERE id = 1;
```

![](https://cdn.hashnode.com/res/hashnode/image/upload/v1721899073857/d60ff63d-18b0-4839-9881-8946954d3cfd.png align="center")

Despite the committed change in transaction 1, transaction 2 still sees the old balance of 70 dollars for account 1. This illustrates that `REPEATABLE READ` ensures read consistency within a transaction.

### Modifying Data in Transaction 2

What happens if we attempt to update the balance in transaction 2?

```sql
-- In transaction 2, subtract 10 from the balance of account 1
UPDATE accounts SET balance = balance - 10 WHERE id = 1;

-- Select account with ID 1 in transaction 2 to verify the change
SELECT * FROM accounts WHERE id = 1;
```

Output:

![](https://cdn.hashnode.com/res/hashnode/image/upload/v1721899143893/812c3454-f1fc-46b1-89a3-eb03ab06b454.png align="center")

The balance is updated to 50 dollars. However, this can be misleading since the previous read in transaction 2 showed a balance of 70 dollars. This discrepancy arises because MySQL allows the update without error, leading to potential inconsistencies within the transaction.

### Rollback and Moving to Serializable

To ensure data consistency, let's rollback transaction 2 and switch to the highest isolation level, `SERIALIZABLE`.

```sql
-- Rollback transaction 2
ROLLBACK;

-- Set the session's transaction isolation level to SERIALIZABLE
SET SESSION TRANSACTION ISOLATION LEVEL SERIALIZABLE;

-- Verify the isolation level
SHOW VARIABLES LIKE 'transaction_isolation';
```

![](https://cdn.hashnode.com/res/hashnode/image/upload/v1721899177443/9f71819c-da11-4059-a2e4-2689b27a88a3.png align="center")

The `REPEATABLE READ` isolation level in MySQL provides a higher degree of consistency compared to `READ COMMITTED`, preventing dirty reads and non-repeatable reads. However, it may still allow certain anomalies, such as phantom reads and inconsistencies during updates. By switching to the `SERIALIZABLE` level, we can achieve full isolation and prevent all such anomalies, ensuring complete data consistency.

## Repeatable Read in **PostgreSQL**

Next, we explore the Repeatable Read isolation level, which ensures that if a transaction reads data, it will always see the same data during its execution.

```sql
-- Transaction 1
BEGIN;
SET TRANSACTION ISOLATION LEVEL REPEATABLE READ;
SHOW TRANSACTION ISOLATION LEVEL;
```

![](https://cdn.hashnode.com/res/hashnode/image/upload/v1721899787987/2a60e364-9b44-42c5-9950-1bedf232f799.png align="center")

```sql
-- Transaction 2
BEGIN;
SET TRANSACTION ISOLATION LEVEL REPEATABLE READ;
SHOW TRANSACTION ISOLATION LEVEL;
```

### Ensuring Non-Repeatable Reads and Phantom Reads are Prevented

Let's perform select operations in both transactions.

```sql
-- Transaction 1
SELECT * FROM accounts;

-- Transaction 2
SELECT * FROM accounts WHERE id = 1;
```

![](https://cdn.hashnode.com/res/hashnode/image/upload/v1721899815839/5e2ab216-e1ac-4777-a2c8-cc484e291837.png align="center")

We then update the balance in Transaction 1 and commit it.

```sql
-- Transaction 1
UPDATE accounts SET balance = balance - 10 WHERE id = 1;
COMMIT;
```

![](https://cdn.hashnode.com/res/hashnode/image/upload/v1721899833233/295f4edf-334d-4688-a327-793d4ba88d63.png align="center")

When we re-run the select queries in Transaction 2, it will still see the old data, preventing non-repeatable reads.

```sql
-- Transaction 2
SELECT * FROM accounts WHERE id = 1;
```

![](https://cdn.hashnode.com/res/hashnode/image/upload/v1721899840711/cf528b6a-1bc6-4e65-9acb-00f11eb38582.png align="center")

### Handling Serialization Anomalies

Finally, let's see how PostgreSQL handles serialization anomalies. We will compute the sum of all account balances and insert a new record with this sum.

![](https://cdn.hashnode.com/res/hashnode/image/upload/v1721899915644/6463fd91-1421-40cc-9a9c-e88a9eef7d32.png align="center")

When both transactions commit, we will see duplicate sum records, indicating a serialization anomaly.

```sql
-- Transaction 1
COMMIT;

-- Transaction 2
COMMIT;

-- Checking the results
SELECT * FROM accounts;
```

### Serializable isolation

The Serializable isolation level guarantees that the outcome of concurrently executed transactions is the same as if the transactions were executed sequentially. This level prevents all common concurrency anomalies, including dirty reads, non-repeatable reads, and phantom reads.

## Serializable isolation in **PostgreSQL**

### Setting Up the Environment

First, let's set up our PostgreSQL environment to test the Serializable isolation level. We will use two transactions and demonstrate how Serializable isolation prevents anomalies.

```sql
-- Transaction 1: Set isolation level to Serializable
BEGIN;
SET TRANSACTION ISOLATION LEVEL SERIALIZABLE;

-- Verify the isolation level
SHOW TRANSACTION ISOLATION LEVEL;

-- Select all accounts and calculate the sum of balances
SELECT * FROM accounts;
SELECT SUM(balance) FROM accounts;

-- Insert a new account with the calculated sum
INSERT INTO accounts (balance) VALUES (810);

-- Commit the transaction
COMMIT;
```

![](https://cdn.hashnode.com/res/hashnode/image/upload/v1721899966202/acee213e-bad1-45bc-8035-dcb93325856f.png align="center")

```sql
-- Transaction 2: Set isolation level to Serializable
BEGIN;
SET TRANSACTION ISOLATION LEVEL SERIALIZABLE;

-- Verify the isolation level
SHOW TRANSACTION ISOLATION LEVEL;

-- Select all accounts and calculate the sum of balances
SELECT * FROM accounts;
SELECT SUM(balance) FROM accounts;

-- Attempt to insert a new account with the calculated sum
INSERT INTO accounts (balance) VALUES (810);

-- Commit the transaction
COMMIT;
```

![](https://cdn.hashnode.com/res/hashnode/image/upload/v1721899963289/2e26565b-d81b-41cf-8ec7-18514f8ffbf1.png align="center")

### Observing the Results

In Transaction 1, we set the isolation level to Serializable, select all accounts, calculate the sum of all balances, and insert a new account with this sum. When we run the same series of queries in Transaction 2, the database prevents a serialization anomaly by throwing an error when we try to commit Transaction 2:

![](https://cdn.hashnode.com/res/hashnode/image/upload/v1721900002479/a9aae96e-9b8d-4e4d-a278-61070ec20006.png align="center")

```plaintext
ERROR: could not serialize access due to read/write dependencies among transactions
HINT: The transaction might succeed if retried.
```

This error indicates that PostgreSQL detected a potential conflict and prevented the transaction from completing, thereby ensuring data consistency.

### Dependency Checking in PostgreSQL

PostgreSQL uses a dependency checking mechanism to maintain Serializable isolation. It tracks dependencies among transactions and detects conflicts that could lead to anomalies. When a conflict is detected, it aborts one of the transactions, ensuring the database remains consistent.

## Serializable Isolation with MySQL

### Setting Up the Environment

Now, let's see how MySQL handles Serializable isolation. We'll use a similar setup with two transactions.

```sql
sqlCopy code-- Transaction 1: Set isolation level to Serializable
SET SESSION TRANSACTION ISOLATION LEVEL SERIALIZABLE;
START TRANSACTION;

-- Select all accounts and calculate the sum of balances
SELECT * FROM accounts;
SELECT SUM(balance) FROM accounts;

-- Insert a new account with the calculated sum
INSERT INTO accounts (balance) VALUES (810);

-- Commit the transaction
COMMIT;
```

![](https://cdn.hashnode.com/res/hashnode/image/upload/v1721899270549/8a46b98a-f277-4870-914c-b9b32e187410.png align="center")

```sql
-- Transaction 2: Set isolation level to Serializable
SET SESSION TRANSACTION ISOLATION LEVEL SERIALIZABLE;
START TRANSACTION;

-- Select all accounts and calculate the sum of balances
SELECT * FROM accounts;
SELECT SUM(balance) FROM accounts;

-- Attempt to insert a new account with the calculated sum
INSERT INTO accounts (balance) VALUES (810);

-- Commit the transaction
COMMIT;
```

![](https://cdn.hashnode.com/res/hashnode/image/upload/v1721899279776/2344f6e2-b42d-4908-88d6-90fad47087cb.png align="center")

### Observing the Results

In MySQL, when Transaction 2 attempts to execute its queries while Transaction 1 is still active, it gets blocked:

![](https://cdn.hashnode.com/res/hashnode/image/upload/v1721899283580/5c66da9a-56ce-4422-a7e7-dac7ea4c9a9f.png align="center")

![](https://cdn.hashnode.com/res/hashnode/image/upload/v1721899297500/5f143173-34de-4517-9d45-ad81ce469ce5.png align="center")

Once Transaction 1 commits, Transaction 2 can proceed with its operations. MySQL uses a locking mechanism to enforce Serializable isolation, ensuring that no anomalies occur. If a deadlock is detected, one of the transactions is aborted, allowing the other to complete.

# Preventing Serialization Anomalies: Theory and Practice

## PostgreSQL: Dependency Checking

PostgreSQL's approach to Serializable isolation relies on detecting and managing dependencies among transactions. When a potential conflict is detected, it aborts one of the conflicting transactions to maintain isolation. This approach ensures that no serialization anomalies occur, but it requires retry logic in the application to handle aborted transactions.

## MySQL: Locking Mechanism

MySQL uses a more traditional locking mechanism to enforce Serializable isolation. When a transaction needs to read or write data, it acquires the necessary locks. If another transaction holds a conflicting lock, the second transaction is blocked until the first one releases its lock. This approach prevents anomalies by ensuring that conflicting transactions do not proceed simultaneously, but it can lead to deadlocks.

# Summary of Isolation Levels and Read Phenomena

## MySQL

| Isolation Level | Dirty Read | Non-Repeatable Read | Phantom Read | Serialization Anomaly |
| --- | --- | --- | --- | --- |
| Read Uncommitted | Yes | Yes | Yes | Yes |
| Read Committed | No | Yes | Yes | Yes |
| Repeatable Read | No | No | Yes | Yes |
| Serializable | No | No | No | No |

## PostgreSQL

| Isolation Level | Dirty Read | Non-Repeatable Read | Phantom Read | Serialization Anomaly |
| --- | --- | --- | --- | --- |
| Read Committed | No | Yes | Yes | Yes |
| Repeatable Read | No | No | No | Yes |
| Serializable | No | No | No | No |

# Conclusion

Understanding and choosing the appropriate isolation level is crucial for maintaining data integrity and performance in your applications. Each database engine has its nuances in implementing these levels, so it's vital to test and document behaviors in your specific context. This guide provided a detailed look at how MySQL and PostgreSQL handle different isolation levels and the implications on data consistency and concurrency.

By experimenting with the provided SQL examples, you can gain hands-on experience and better appreciate the intricacies of database transaction isolation levels. Always refer to the official documentation of MySQL and PostgreSQL for more in-depth information and updates.