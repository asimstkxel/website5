---
name: qa
description: Quality assurance, test planning, test case design, automated testing, bug verification, regression checks, and quality review. Use for writing tests, verifying fixes, reviewing quality, or building test automation.
---

# Quality Assurance

## Use this skill when

- Writing or reviewing test plans and test cases
- Building automated tests (unit, integration, e2e)
- Verifying bug fixes and running regression checks
- Reviewing code quality and identifying defects
- Designing test strategies for new features
- Assessing test coverage and identifying gaps

## Do not use this skill when

- The task is purely about writing production code (route to backend or frontend)
- The task is about gathering requirements (route to business-analyst)

## Instructions

- Start from acceptance criteria or requirements when available
- Prioritize tests by risk and business impact
- Write tests that are independent, repeatable, and deterministic
- Prefer testing behavior over implementation details

## Test Strategy

### Test Pyramid

Follow the test pyramid to balance speed and confidence:

```
        /  E2E  \          Few, slow, high-confidence
       /----------\
      / Integration \      Moderate count, test boundaries
     /----------------\
    /    Unit Tests     \  Many, fast, isolated
```

- **Unit tests**: Test individual functions, components, and modules in isolation. Mock external dependencies. These run fast and catch logic errors early.
- **Integration tests**: Test interactions between modules, API endpoints with a real database, or component trees with real state. Catch contract and wiring issues.
- **E2E tests**: Test critical user flows end-to-end through the real application. Keep these few and focused on high-value paths.

### What to test

- Happy path: the expected behavior works correctly
- Edge cases: empty inputs, boundary values, max lengths, special characters
- Error handling: invalid inputs, network failures, unauthorized access, timeouts
- State transitions: loading, success, error, empty states
- Accessibility: keyboard navigation, screen reader compatibility, focus management
- Performance: response times under load, rendering performance, memory leaks

## Test Case Design

### Format

```
Test ID: TC-[feature]-[number]
Title: [concise description of what is being tested]
Preconditions: [required state before test execution]
Steps:
  1. [action]
  2. [action]
Expected Result: [observable outcome]
Priority: Critical | High | Medium | Low
Type: Unit | Integration | E2E | Manual
```

### Techniques

- **Equivalence partitioning**: Divide inputs into groups that should behave the same; test one from each group.
- **Boundary value analysis**: Test at the edges of valid ranges (min, min+1, max-1, max, and just outside).
- **Decision tables**: Map combinations of conditions to expected outcomes for complex business logic.
- **State transition testing**: Verify valid and invalid transitions between states.

## Automated Testing Patterns

### Unit Test Structure (Arrange-Act-Assert)

```typescript
describe('calculateDiscount', () => {
  it('applies 10% discount for orders over $100', () => {
    // Arrange
    const order = { total: 150, customerTier: 'standard' };

    // Act
    const result = calculateDiscount(order);

    // Assert
    expect(result).toBe(135);
  });

  it('returns original total for orders under $100', () => {
    const order = { total: 50, customerTier: 'standard' };
    const result = calculateDiscount(order);
    expect(result).toBe(50);
  });

  it('throws for negative totals', () => {
    const order = { total: -10, customerTier: 'standard' };
    expect(() => calculateDiscount(order)).toThrow('Invalid total');
  });
});
```

### Component Test Pattern

```typescript
describe('LoginForm', () => {
  it('disables submit button when fields are empty', () => {
    render(<LoginForm />);
    expect(screen.getByRole('button', { name: /sign in/i })).toBeDisabled();
  });

  it('shows validation error for invalid email', async () => {
    render(<LoginForm />);
    await userEvent.type(screen.getByLabelText(/email/i), 'notanemail');
    await userEvent.click(screen.getByRole('button', { name: /sign in/i }));
    expect(screen.getByText(/invalid email/i)).toBeInTheDocument();
  });

  it('calls onSubmit with credentials on valid submission', async () => {
    const onSubmit = vi.fn();
    render(<LoginForm onSubmit={onSubmit} />);
    await userEvent.type(screen.getByLabelText(/email/i), 'user@test.com');
    await userEvent.type(screen.getByLabelText(/password/i), 'securepass');
    await userEvent.click(screen.getByRole('button', { name: /sign in/i }));
    expect(onSubmit).toHaveBeenCalledWith({
      email: 'user@test.com',
      password: 'securepass',
    });
  });
});
```

### API Integration Test Pattern

```typescript
describe('POST /api/users', () => {
  it('creates a user and returns 201', async () => {
    const res = await request(app)
      .post('/api/users')
      .send({ email: 'new@test.com', name: 'Test User' });

    expect(res.status).toBe(201);
    expect(res.body.data).toMatchObject({
      email: 'new@test.com',
      name: 'Test User',
    });
  });

  it('returns 400 for duplicate email', async () => {
    await createUser({ email: 'dup@test.com' });
    const res = await request(app)
      .post('/api/users')
      .send({ email: 'dup@test.com', name: 'Dup User' });

    expect(res.status).toBe(400);
    expect(res.body.error.code).toBe('VALIDATION_ERROR');
  });

  it('returns 400 for missing required fields', async () => {
    const res = await request(app).post('/api/users').send({});
    expect(res.status).toBe(400);
  });
});
```

## Bug Verification Process

1. **Reproduce**: Confirm the bug exists using the reported steps. Document the actual vs expected behavior.
2. **Characterize**: Write a failing test that captures the bug. This test must fail before the fix and pass after.
3. **Verify fix**: After the fix is applied, run the characterization test and confirm it passes.
4. **Regression check**: Run the full test suite to ensure the fix did not break other functionality.
5. **Edge cases**: Test related scenarios near the bug to catch similar issues.

## Quality Review Checklist

- [ ] All acceptance criteria have corresponding tests
- [ ] Tests cover happy path, error cases, and edge cases
- [ ] No test depends on another test's state or execution order
- [ ] Tests use meaningful assertions (not just "no error thrown")
- [ ] Mocks and stubs are minimal and only used at boundaries
- [ ] Test names clearly describe the behavior being verified
- [ ] No hardcoded waits or sleeps (use proper async patterns)
- [ ] Test data is created fresh per test, not shared mutably
- [ ] Coverage meets project thresholds (aim for meaningful coverage, not 100%)
- [ ] Flaky tests are identified and fixed, not skipped

## Reporting

When reporting QA results back to the orchestrator or user:

```
## QA Report: [feature/fix name]
**Status:** Pass | Fail | Blocked
**Tests written:** [count by type]
**Tests passing:** [count]
**Tests failing:** [count, with details]
**Coverage:** [relevant metrics]
**Findings:** [bugs found, risks identified, or "none"]
**Recommendation:** [ship / fix before shipping / needs more testing]
```
