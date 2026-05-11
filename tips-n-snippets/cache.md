# Cache

## Summary

Cache is a technique used to store frequently accessed data temporarily so it can be retrieved faster.

Instead of recalculating or fetching data from a slow source every time, the system reads from the cache when possible.

Cache is commonly used in APIs, databases, web applications, distributed systems, AI systems, and high-scale platforms.

## When to Use

Use cache when you need to:

- Improve response time
- Reduce database load
- Reduce external API calls
- Reuse expensive computations
- Improve scalability
- Reduce infrastructure cost
- Handle high traffic more efficiently

## How It Works

```text
Client requests data
    ↓
System checks cache
    ↓
If data exists, return from cache
    ↓
If data does not exist, fetch from source
    ↓
Store result in cache
    ↓
Return response
```

## Common Cache Types

### In-Memory Cache

Stores data in application memory.

```text
Fast, but local to one application instance
```

### Distributed Cache

Stores data in an external cache service.

```text
Redis
Memcached
```

Useful when multiple services or instances need shared cached data.

### CDN Cache

Stores static content close to users.

```text
Images
CSS
JavaScript
Static files
API responses
```

### AI Cache

Stores expensive AI-related results.

```text
LLM responses
Embeddings
Vector search results
Prompt results
Model outputs
```

## Common Strategies

### Cache Aside

The application checks the cache first.

```text
Cache miss → fetch from database → save in cache
```

### Write Through

Data is written to cache and database together.

```text
Write to cache → write to database
```

### TTL

TTL means Time To Live.

It defines how long cached data remains valid.

```text
cache expires after 5 minutes
```

## Benefits

- Faster responses
- Lower database load
- Lower API costs
- Better scalability
- Better user experience
- Useful for expensive AI operations

## Challenges

- Stale data
- Cache invalidation complexity
- Extra infrastructure
- Memory usage
- Harder debugging
- Inconsistent data if poorly managed

## Related Concepts

```text
scalability.md
high-availability.md
distributed-architecture.md
redis.md
api-versioning.md
personalization.md
```

## Simple Explanation

```text
Cache stores data temporarily
so the system can reuse it faster
instead of fetching or computing it again.
```