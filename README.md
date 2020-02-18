# Bloom Filter
This is my implementation of a bloom filter using Python 3.

## What is a Bloom Filter?
A bloom filter is an efficient way of determining whether a given set contains a specific element, conceived by **Burton Howard Bloom**. However, Bloom Filters are probabilistic and trade accuracy for efficiency; a Bloom Fitler may produce false positives, but will never produce a false negative. In other words, a Bloom Filter can tell you that an element is *definitely* not in a set, but it cannot be 100% sure that an element *is* in a set. 

## What's it for?
Imagine you have a website with lots of users. When a new user wants to join, they have to create a username and account. Now, you can't have 2 users with the same username, so some checks need to be performed to make sure it is unique. Searching through all the usernames in your database can be very time consuming. A bloom filter would provide a much faster way to check if that username already exists. 

## How does it work?
Bloom Filters use a fixed-size bit array *A*, with all bits set to 0, to keep track of entries in the filter. Let's say the size of the array is *m*. Each entry is hashed and the resulting value, let's call it *v*, must be transformed in a way so that *v* is less than *m*. This can be acheived using the modulo operator. We'll call this *i* so *0 < i < m*. We then set *A<sub>i</sub>* to 1. 

#### Here's an example: 

Let's start with a 8 bit (1 byte) array *A*:
`[0,0,0,0,0,0,0,0]`
So *m = 10*.
We have a hash function *f*.
We want to add the word "hello" to our set.
We run the work through the hash function: `f("hello") = 23`.
Then we need to use modulo on the value: `23 % m = 3`.
Now we've got `3`, so we'll set *A<sub>3</sub>* to 1. 
`[0,0,0,1,0,0,0,0]`
> Note: Arrays start from 0, not 1.

Let's add the word "world" to the set now: `f("world") = 45`.
We'll use modulo again: `45 % m = 5`.
And we'll set *A<sub>5</sub>* to 1.
`[0,0,0,1,0,1,0,0]`

This is a really simple example, but you can see how we've reduced the size of the information. "hello" and "world" are 5 bytes each, but we've created something that can test for these words in a single byte.

#### Here's the main problem with Bloom Filters:
So we've got our bit array: 
`[0,0,0,1,0,1,0,0]`
We want to check if the word "foo" is in the set.
So we use the same hash function to search: `f("foo") = 15`
We'll use modulo to get an index: `15 % m = 5`
Then we'll check the value in the bit array at index 5.
`[0,0,0,1,0,`<strong>`1`</strong>`,0,0]`
The bit at index 5 is set to 1. This is one of those false positives mentioned at the beginning, and demonstrates why Bloom Filters can never be certain that an element is in the set.