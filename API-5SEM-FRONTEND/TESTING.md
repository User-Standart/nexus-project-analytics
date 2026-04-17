# Unit Testing Guide — Frontend (Nuxt.js)

## Overview

This document defines the unit testing standard for the API-5SEM frontend.
As a DevOps practice, one example has been implemented. Developers must replicate this pattern for each new feature they implement.

---

## Rules

- Test files go inside `app/tests/`
- Test file name: `<feature>.spec.ts`
- Every feature must have **at least 2 scenarios**: success + edge case
- Tests must follow the **AAA pattern**: Arrange → Act → Assert
- Tests must be submitted in the **same PR** as the feature
- If CI fails, the **PR author** is responsible for fixing it

---

## Pattern

### 1. Create the test file

Inside `app/tests/`, create `yourfeature.spec.ts`.

### 2. Write the tests

```ts
import { describe, it, expect } from 'vitest'

// The function you want to test
function myFunction(input: string): string {
  return input.trim()
}

describe('myFunction', () => {
  // Success scenario
  it('removes whitespace from string', () => {
    // Arrange
    const input = '  hello  '

    // Act
    const result = myFunction(input)

    // Assert
    expect(result).toBe('hello')
  })

  // Edge case
  it('returns empty string when input is empty', () => {
    expect(myFunction('')).toBe('')
  })
})
```

### 3. Run the tests

```bash
# Run all tests
pnpm test

# Run in watch mode (re-runs on save)
pnpm vitest
```

---

## Reference example

See [`app/tests/StatCard.spec.ts`](./app/tests/StatCard.spec.ts) for a complete working example.
