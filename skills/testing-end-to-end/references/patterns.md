# E2E patterns

The examples below use Playwright Test and were last checked on 2026-09-28. Check names against the installed version's docs or `--help` before copying them. Other runners have equivalent features under different names.

## Reusing auth state

Log in once in a setup project, save the browser storage, and load it in the other tests.

```ts
// tests/auth.setup.ts
import { test as setup, expect } from '@playwright/test';

setup('authenticate', async ({ page, request }) => {
  await page.goto('/login');
  await page.getByLabel('Email').fill(process.env.E2E_USER!);
  await page.getByLabel('Password').fill(process.env.E2E_PASSWORD!);
  await page.getByRole('button', { name: 'Sign in' }).click();
  await expect(page.getByRole('navigation')).toContainText('Account');
  await page.context().storageState({ path: 'playwright/.auth/user.json' });
});
```

Wire it up in the config: a `setup` project that matches `auth.setup.ts`, and browser projects with `dependencies: ['setup']` and `use: { storageState: 'playwright/.auth/user.json' }`. Add `playwright/.auth/` to `.gitignore`. Credentials come from environment variables and are never committed.

## Waiting for the response an action triggers

```ts
const saved = page.waitForResponse(r => r.url().includes('/api/orders') && r.request().method() === 'POST');
await page.getByRole('button', { name: 'Place order' }).click();
expect((await saved).status()).toBe(201);
await expect(page.getByRole('status')).toHaveText(/Order #\d+ confirmed/);
```

Start waiting *before* the click, so a fast response is not missed.

## Isolated test data

```ts
import { test as base } from '@playwright/test';

type Fixtures = { customer: { id: string; email: string } };

export const test = base.extend<Fixtures>({
  customer: async ({ request }, use) => {
    const email = `e2e+${crypto.randomUUID()}@example.test`;
    const res = await request.post('/api/test/customers', { data: { email } });
    const customer = await res.json();
    await use(customer);
    await request.delete(`/api/test/customers/${customer.id}`);
  },
});
```

The test-data endpoint (or a seed script) exists only in test environments. Guard it by environment and never deploy it to production.

## Stubbing a third party at the network edge

```ts
await page.route('https://api.maps.example.com/**', route =>
  route.fulfill({ json: { lat: 52.52, lng: 13.405 } }));
```

Stub only hosts you do not own. Record which ones are stubbed in the suite README.

## CI

- Run all specs in CI with parallel workers or shards. Locally, run one spec with one worker.
- Capture a trace on the first retry, and screenshots and video on failure. Upload them as CI artifacts.
- Allow at most one retry, and report retried passes as flaky so they get triaged rather than ignored.
- Start the app with the runner's web-server option, or a wrapper that waits for the port, so tests never race the server's startup.
