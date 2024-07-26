---
title: "Decoding RabbitMQ: Enhancing Communication in Distributed Systems with Message Brokers"
seoTitle: "Decoding RabbitMQ"
seoDescription: "Architecture of Message Queuing RabbitMQ,  Fundamentals of RabbitMQ, AMQP Protocol, and Fail-Safe Messaging Strategies for Robust System Integration"
datePublished: Sun Feb 11 2024 19:55:23 GMT+0000 (Coordinated Universal Time)
cuid: clshxd9uu000108jtdjzfce8b
slug: decoding-rabbitmq-exploring-the-architecture-of-message-queuing
cover: https://cdn.hashnode.com/res/hashnode/image/upload/v1707681033114/d7ddd115-37a3-4994-8a77-27d034973b95.png
tags: message-queue, rabbitmq

---

> **RabbitMQ is the most widely deployed open source message broker.**

With tens of thousands of users, RabbitMQ is one of the most popular open source message brokers. From [T-Mobile](https://www.youtube.com/watch?v=1qcTu2QUtrU) to [Runtastic](https://medium.com/@runtastic/messagebus-handling-dead-letters-in-rabbitmq-using-a-dead-letter-exchange-f070699b952b), RabbitMQ is used worldwide at small startups and large enterprises.

RabbitMQ is lightweight and easy to deploy on premises and in the cloud. It supports multiple messaging protocols and [streaming](https://www.rabbitmq.com/streams.html). RabbitMQ can be deployed in distributed and federated configurations to meet high-scale, high-availability requirements.

RabbitMQ runs on many operating systems and cloud environments, and provides a [wide range of developer tools for most popular languages](https://www.rabbitmq.com/devtools.html).

Now let's dive deeper into RabbitMQ:

# **Understanding RabbitMQ and Message Brokers**

## **Introduction to Message Brokers**

### What is a Message Broker?

RabbitMQ is a message broker. So, what is a message broker? A message broker is a software that enables applications, systems, and services to communicate with each other and exchange information.

![](https://cdn.hashnode.com/res/hashnode/image/upload/v1707680781915/d23ee53f-06b9-4b68-a1cb-5f8c870889ed.png align="center")

## **Use Cases of Message Brokers**

### Communication Between Processes

Say there is a Process P1 and P2. You want them to communicate. This can happen with Shared Resources, REST API calls or Message Brokers!

### Microservice Architecture Integration

Another prominent use case is in Microservice Architecture. Say there is one Service S1 and S2, running on different servers. These can communicate with REST API or RPC or Message Brokers. This message broker is a <mark>Message Queue</mark>.

> In [computer science](https://en.wikipedia.org/wiki/Computer_science), [a **queue** is a co](https://en.wikipedia.org/wiki/Computer_science)[llection of entitie](https://en.wikipedia.org/wiki/Collection_(abstract_data_type))s that are maintained in a sequence and can be modified by the addition of entities at one end of the sequence and the removal of entities from -the other end of the sequence.
> 
> * Source: Wikipedia
>     

Suppose, there is a Server S3 that hosts our message Broker. Now, S1 will push the message to a queue and S2 will take the input from the Queue. In technical words, S1 is **Publisher** or Producer and S2 is Consumer.

Rabbit MQ supports various protocols, such as AMQP 091, AMQP 10, MQTT, and STOMP. AMQP 091 is the most popular protocol. Let's Understand what it is.

## **Overview of AMQP Protocol**

### The OSI Model and Networking Layers

AMPQ is an application layer protocol. Say, there's Process P1 written in Go and Process P2 in C# on different servers. P1 wants to send a Packet or Message to P2. How will this communication happen? It happens with some set of rules. Just like how real-life communication has language, a medium and Energy conversion, similar things happen here. A set of protocols ensures that this communication is language agnostic.

These protocols happen in various layers in the computer. This has been standardized into 7 layers called as OSI model of networking.

[![What is the OSI Model? | Cloudflare](https://cf-assets.www.cloudflare.com/slt3lc6tev37/6ZH2Etm3LlFHTgmkjLmkxp/59ff240fb3ebdc7794ffaa6e1d69b7c2/osi_model_7_layers.png align="left")](https://www.cloudflare.com/en-gb/learning/ddos/glossary/open-systems-interconnection-model-osi/)

The last 3 layers are software layers. The transport Layer is the Heart of OSI and the first 3 are somewhat hardware layers. At the transport layer, there is TCP/UDP. At the network layer, there is UDP. Transport, Network and Data Link are responsible for routing messages. Session related to behavioural layer. Application and Presentation are generally used directly or indirectly by us, Software Developers!

Say you want to hit the rest API of Service 2. You will use the requests module from Pythion. In that module, there is code to interact with Layer 6/7. Say you want to connect with an IP address and send some Payload on this protocol, your request module, will make a Data Packet with Protocol info, IP address, destination Address, source address, and payload. Once a packet is created, it moves through the next layers. Here, your code won't interfere and instead trigger commands of the Operating System. Now OS code will run on these layers and every layer will add some new information.

It might be also possible that the packet is large suck that it is not possible to transport it as a whole. Now, the Network layer breaks the packet into multiple small packets and will add extra info to each packet.

Coming back to AMQP 091, which is an application layer protocol. Say there's a client who wants to communicate to service with RMQ running. If a client wants to communicate with RMQ, it will also have to follow the same protocol that RMQ is following. All this is already developed and abstracted in some library or package. All we have to do is to import this library, and it takes care of everything. This library is called the Client Library. In python, there's [a Pika](https://pika.readthedocs.io/en/stable/intro.html) module available

### AMQP 0.9.1 Protocol Explained

The message constructed at the application [layer](https://pika.readthedocs.io/en/stable/intro.html) has various information that [AMQP](https://pika.readthedocs.io/en/stable/intro.html) demands. Say, there is a publisher P1 and consumer C1 and another server with RMQ. The message broker (RMQ) built over AMPQ 091 is expected to have certain components namely Exchange and Queues.

![Publish path from publisher to consumer via exchange and queue](https://www.rabbitmq.com/img/tutorials/intro/hello-world-example-routing.png align="center")

The publisher publishes the message. the message is sent to Exchange. The responsibility of exchange is to route this message to the queues that it has to. Then the consumer can listen to any queue.

At packet formation at the Application layer, it also will have information about the exchange. It's also possible that it has information about the queue or the connection. So, if the message broker doesn't have an exchange or queue, it won't be able to decode this packer properly.

AMQP 091 expects this kind of model.

---

## **Delving into RabbitMQ**

### Publisher-Consumer Communication Model

Till now you have read how the AMQP protocol works and what kind of model it expects. Now let's delve specifically into RabbitMQ, how it works and uses AMQP protocol.

The Publisher and Consumer act as clients for the broker. They act as an interface between the broker and the application in order to receive packets that are coming from queues.

### Connection Establishment and Channel Creation

The first thing that happens is that the publisher will try to establish a connection with the broker. This is done with the help of the client library by providing the server. We will specify the host and protocol (AMQP). Now, the client library will make a Packet at the application layer, then it will be passed via the OSI model and each layer will add more information. At the transport layer, AMQP uses TCP protocol. TCP plays an important role in establishing the connection.

When you make a socket connection with TCP, first a TCP packet is sent, called SYN. RabbitMQ server sends SYN + ACK back. Then, the client sends ACK and a TCP connection is established. Now, a TCP connection is established. This process is called a TCP 3-way handshake. The total packets excluding those mentioned above are 7. Everything is taken care of by the Operating System! Since TCP has acknowledgements, it is highly reliable. But, it also makes it slow.

Even if you are using TLS, which is SSL protection, before sending to RMQ, it will also involve more packets before establishing the connection.

![12 TCP Transport — An Introduction to Computer Networks](https://lh6.googleusercontent.com/proxy/ZflJhXAc3RW7zLQM8ud7LCRDv7eRhMVatNHbBHg_NB0SgMiZhsnQ8np9OPj6iVnZmPSq8YYUTXUubh8fj4osN_pM73mdDc3hhdFpbGBUTLJfrsDFW0R6 align="center")

Now that, the connection is established, we will also have to make a channel. After establishing a connection, we can create multiple channels with the same connection. So, this connection can be multiplexed. To create this channel, it involves 2 TCP packets.

Now, you can create an Exchange from RMQ UI. After establishing the connection and creating the Exchange you can publish a message to the exchange. This Publish also requires 1 TCP packet plus acknowledgement. While publishing you have to provide the exchange name and the payload which we want to send.

But while publishing the message, more information is needed. because the Exchange can be of many types.

### Exchange Types in RabbitMQ

1. Direct Exchange: Let's say you created Queue Q1 and want to bind this Queue to Exchange. So, in order to make a connection a binding is required. For binding, a routing/ binding key is required. Say, the routing key is 'P1.Q1.msg'. When publishing the message, one more parameter is the routing Key. In the above case, it is 'P1.Q1.msg'.
    
2. Default Exchange: When we start RabbitMQ, it normally has a default exchange. When we publish msg to the default exchange, it will create the Queue with the name of the routing key provided and the binding will also have the same name as the Routing Key
    
3. Topic Exchange: It is similar to direct exchange, but has more flexibility. Say, you want to send a message to `N` Queues directly, it can happen over direct exchange because it has the functionality of Regex with # and \*. So, all Queues bounded with exchange with Routing key satisfying the REGEX expression will receive that message
    
4. Fanout Exchange: In this one, the routing key is ignored and all the queues attached to the exchange will receive that message. It is useful in Broadcasting.
    
5. Header Exchange: In the case of Topic and Direct Exchange, we were using the routing key to route the message. But this uses the header to route the message. We need to specify the headers, which have key-value pairs. Since by default, it is configured in such a way that all the headers specified in the Publish method should match the bindings. There's a property called `X_match` whose value is `ALL`. In case no header matches, then no message will route to that queue
    
6. Dead Letter/ Alternate Exchange: It is sometimes desirable to let clients handle messages that an exchange was unable to route (i.e. either because there were no bound queues or no matching bindings). Typical examples of this are
    
    * **detecting when clients accidentally or maliciously publish messages that cannot be routed**
        
    * **"or else" routing semantics where some messages are handled specially and the rest by a generic handler**
        
    
    Alternate Exchange ("AE") is a feature that addresses these use cases.
    

Till now we covered how the connection is established and how the message is routed from exchange to queue. Now let's see how Queue forwards the message to the consumer

Say, the consumer is listening to Queue Q1, then Q1 will forward those messages to this consumer. Specific to RabbitMQ, it provides flexibility to create Queue and Exchange from the client itself and change the configuration from the client itself. That's why it is highly flexible yet user-friendly!

---

## **Handling Message Transmission and Failures**

To understand each point of failure, we will go from a backward direction and cover every point of failure and how to handle it. Suppose the consumer has made a connection with Queue with Topic exchange. The binding has a routing key.

[![](https://cdn.hashnode.com/res/hashnode/image/upload/v1707813667006/33b28ea1-7eb0-4300-a83b-9efb152ca0d7.jpeg align="center")](https://www.cloudamqp.com/blog/part1-rabbitmq-best-practice.html)

1. Assume a scenario, that a message is pushed from Queue Q2 to the consumer and Q2 removes the message, but the consumer server is down or the TCP connection is broken. Here, the mechanism of acknowledgement is used at the AMQP level (along with TCP connection acknowledgements). This mechanism is asynchronous ensuring speed. It is done in 2 ways:
    
    1. Auto ACK: By default, the Queue won't wait for ACK from the consumer. This message is automatically acknowledged. This thing is fine when a message is not that important, like Promotional mail! It is also faster and relatively
        
    2. Manual ACK: Say the publisher publishes a message exactly once, and we need to make sure that the consumer consumes the message and performs certain operations on that. In such situations, Manual ACK is preferred. Aside from TCP level ACK, AMQP level ACK is sent after completing operations on the message. After receiving AMQP level ACK, the message is removed from Queue.
        
        1. One edge case is that the Consumer performs operations but fails to send the ACK. The same message might be sent more than once. We need to make sure that the consumer handles those repetitive cases.
            
        2. One more edge case is that because of high loads, the consumer is still processing those messages, but the duration for which the Queue waits for ACK has crossed. The Queue pushes that message again. In such cases, DB Logs come in handy. This is called Idempotency
            

> **Idempotence**[is](https://en.wikipedia.org/wiki/Idempotence#cite_note-2)[th](https://en.wikipedia.org/wiki/Help:IPA/English)e property of certain [operations in mathema](https://en.wikipedia.org/wiki/Operation_(mathematics))[tics and compute](https://en.wikipedia.org/wiki/Mathematics)[r science whereby they can](https://en.wikipedia.org/wiki/Computer_science) be applied multiple times without changing the result beyond the initial application.
> 
> * Source: [Wikipedia](https://en.wikipedia.org/wiki/Idempotence)
>     

1. Assume the Consumer sends ACK, but the RabbitMQ server crashes before receiving the ACK. Since we are using TCP, the TCP connection is broken and the message is lost completely. For this, RabbitMQ provides one feature called Durable Queues and Persistent Message. In this case, this message will be stored in Disk or some permanent memory. When we restart the Broker again, it will see that ACK hasn't received so it will again push that message to Queue. That message was already processed by Consumer but that's fine because our Consumer is Idempotent. This ACK can be done in Bulk too.
    
2. There is a possibility that the Consumer Rejects the message. For rejecting there are two options:
    
    1. `NACK`: This was introduced to reject messages in Bulk
        
    2. `Reject`: This can reject only one message at a time
        
    
    After rejection, the Queue can Request and send the message to a different consumer. This works when there are multiple consumers but for a single consumer, it might go into an infinite loop. Such a message can be queued or discarded or routed to Alternate Exchange. Alternate Exchange might also have certain Queues to which we can set a consumer
    
3. Now assume, the Publisher sends a message to Exchange but the server is down, so the TCP connection is broken and the message gets lost. For this `Publisher Confirms` saves the day. It is sort of an Acknowledgement. ACK is sent when Exchange has successfully routed the message to dedicated Queues. It can be achieved Synchronously or using Batches or Asynchronously
    
4. What if there are no Queues corresponding to the Routing key? This is a case of an unrouteable message.
    
    In this case, we can set up an Alternate Exchange.
    

All these are major things which make RabbitMQ reliable!

---

# **Wrapping Things Up**

Wow, what a journey it's been diving into the world of RabbitMQ and message brokers. Let's take a moment to summarize everything we've learned in a more casual way.

### Conclusion

Alright, let's break it down. RabbitMQ? It's like the super-smart middleman that makes sure all your computer stuff can chat with each other without any hiccups. Think of it as the glue holding your digital world together.

Remember that AMQP protocol we talked about? It's kind of like RabbitMQ's playbook, showing it exactly how to handle messages and get them where they need to be. Like a coach guiding their team to victory!

And those different exchange types? They're like RabbitMQ's bag of tricks. Need to send a message straight to the target or broadcast it to a whole bunch of places? RabbitMQ's got your back, with options for every scenario.

But what about when things don't go as planned? No worries! RabbitMQ's got some ninja moves for handling tricky situations. It can stash messages away safely and make sure they still get delivered, even if there's a bump in the road.

So, yeah, RabbitMQ might seem a bit daunting at first glance, but once you get to know it, it's like having a trusty sidekick keeping your digital world ticking along smoothly.

---