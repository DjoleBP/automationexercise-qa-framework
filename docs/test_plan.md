# Test Plan

This document is the TestRail/TestLink stand-in for this project (see README for why). It
lists every implemented, automated test case: ID, title, type, priority, preconditions, steps,
and expected result. It is kept in sync with the actual test suite under `tests/` — if a test
is renamed, removed, or its behavior changes, this table is updated in the same change.

**Target under test:** [automationexercise.com](https://automationexercise.com)
**Automation:** Playwright (Python) for UI, `requests` for API — see `pytest.ini` for the
`smoke` / `functional` / `regression` / `negative` / `api` / `mobile` markers used as "Type" below.

## UI test cases (`tests/ui/`)

| ID | Title | Type | Priority | Preconditions | Steps | Expected Result |
|----|-------|------|----------|----------------|-------|------------------|
| TC-UI-001 | Homepage loads | smoke | High | None | 1. Navigate to `/` | Page title contains "Automation Exercise"; logo is visible |
| TC-UI-002 | Register new user with valid data | smoke | High | None (Faker generates a unique email) | 1. Go to Login/Signup page 2. Enter name + unique email, submit 3. Fill account information form 4. Submit | "ACCOUNT CREATED!" is shown; after continuing, "Logged in as \<name\>" is visible in the nav |
| TC-UI-003 | Register with an already-registered email | negative | High | A user account already exists (`registered_user` fixture) | 1. Go to Login/Signup page 2. Enter a name and the existing email 3. Submit | "Email Address already exist!" is shown; no account is created |
| TC-UI-004 | Login with valid credentials | smoke | High | A user account exists (`registered_user` fixture) | 1. Go to Login page 2. Enter valid email + password 3. Submit | "Logged in as \<name\>" is visible in the nav |
| TC-UI-005 | Logout returns to logged-out state | smoke | High | Logged in (`logged_in_page` fixture) | 1. Click Logout | Redirected to the login page; "Signup / Login" link is visible again |
| TC-UI-006 | Login with wrong password | negative | High | A user account exists | 1. Go to Login page 2. Enter valid email + wrong password 3. Submit | "Your email or password is incorrect!" is shown; user is not logged in |
| TC-UI-007 | Login with unregistered email | negative | Medium | None | 1. Go to Login page 2. Enter an email that was never registered + any password 3. Submit | "Your email or password is incorrect!" is shown |
| TC-UI-008 | Search for an existing product | smoke | High | None | 1. Go to Products page 2. Search "Top" | "Searched Products" heading shown; at least one result; results relate to "top" (name or category) |
| TC-UI-009 | Search with no matching results | negative | Medium | None | 1. Go to Products page 2. Search a nonsense term | "Searched Products" heading shown with zero product cards (graceful empty state) |
| TC-UI-010 | Product details page shows expected fields | regression | Medium | None | 1. Open a product's details page | Name, category, price, availability, condition, and brand are all visible |
| TC-UI-011 | Category filter returns filtered results | regression | Medium | None | 1. Go to Products page 2. Expand a category group in the sidebar accordion 3. Click a subcategory | At least one product card is shown |
| TC-UI-012 | Brand filter returns filtered results | regression | Medium | None | 1. Go to Products page 2. Click a brand in the sidebar | At least one product card is shown, all under that brand |
| TC-UI-013 | Add product to cart with a specific quantity | smoke | High | None | 1. Open a product's details page 2. Set quantity to 4 3. Add to cart 4. View cart | Cart has 1 row for that product with quantity "4" |
| TC-UI-014 | Add multiple different products to cart | functional | High | None | 1. Go to Products page 2. Add two different products to cart (closing the confirmation modal between adds) 3. View cart | Cart has 2 rows, one per product |
| TC-UI-015 | Remove item from cart | functional | High | None | 1. Add a product to cart 2. View cart 3. Click remove on that row | Row is removed; after a reload, "Cart is empty!" is shown |
| TC-UI-016 | "Recommended items" carousel appears | regression | Low | None | 1. Go to the homepage 2. Scroll to the recommended items section | Section is visible. **Note:** the official site test case (#22) documents this on `/view_cart`; live verification found it only renders on the homepage — see the linked GitHub issue |
| TC-UI-017 | Checkout flow through to order confirmation | smoke | High | Logged in, product in cart | 1. Proceed to checkout 2. Add an order comment 3. Place order 4. Fill dummy payment details 5. Pay | "Order Placed!" confirmation is shown |
| TC-UI-018 | Submit Contact Us form with valid data | smoke | High | None | 1. Go to Contact Us page 2. Fill name/email/subject/message 3. Submit (accepting the confirm dialog) | Success alert "Success! Your details have been submitted successfully." is shown |
| TC-UI-019 | Submit Contact Us form with required fields empty | negative | Medium | None | 1. Go to Contact Us page 2. Submit without filling any field | No success message appears; user stays on `/contact_us` |
| TC-UI-020 | Subscribe to the newsletter footer widget | smoke | Medium | None | 1. Go to homepage 2. Scroll to footer 3. Enter a unique email 4. Click subscribe | "You have been successfully subscribed!" is shown |
| TC-UI-021 | Homepage loads under mobile emulation | mobile / smoke | High | iPhone 13 device emulation | 1. Open homepage on emulated mobile viewport | Title correct; logo visible |
| TC-UI-022 | Product browsing under mobile emulation | mobile / functional | Medium | iPhone 13 device emulation | 1. Open Products page on emulated mobile viewport | "All Products" heading and product cards are visible |
| TC-UI-023 | Search under mobile emulation | mobile / functional | Medium | iPhone 13 device emulation | 1. Open Products page 2. Search "Top" on emulated mobile viewport | "Searched Products" heading and results are visible |

## API test cases (`tests/api/`)

| ID | Title | Type | Priority | Preconditions | Steps | Expected Result |
|----|-------|------|----------|----------------|-------|------------------|
| TC-API-001 | Create and delete an account | smoke / api | High | None | 1. `POST /api/createAccount` with a unique user 2. `DELETE /api/deleteAccount` | `responseCode` 201 "User created!"; then `responseCode` 200 "Account deleted!" |
| TC-API-002 | Create account with already-registered email | negative / api | Medium | An account already exists for the email | 1. `POST /api/createAccount` with a duplicate email | `responseCode` 400, message "Email already exists!" |
| TC-API-003 | Get brands list | smoke / api | High | None | 1. `GET /api/brandsList` | `responseCode` 200; non-empty `brands` array, each with `id` and `brand` |
| TC-API-004 | Brands list rejects PUT | negative / api | Medium | None | 1. `PUT /api/brandsList` | `responseCode` 405, "method is not supported" |
| TC-API-005 | Verify login with valid credentials | smoke / api | High | An account exists | 1. `POST /api/verifyLogin` with correct email + password | `responseCode` 200, message "User exists!" |
| TC-API-006 | Verify login with invalid credentials | negative / api | High | None | 1. `POST /api/verifyLogin` with a non-existent email | `responseCode` 404, message "User not found!" |
| TC-API-007 | Verify login with missing password | negative / api | Medium | None | 1. `POST /api/verifyLogin` with only an email | `responseCode` 400, "email or password parameter is missing" |
| TC-API-008 | Verify login rejects DELETE | negative / api | Low | None | 1. `DELETE /api/verifyLogin` | `responseCode` 405, "method is not supported" |
| TC-API-009 | Get products list | smoke / api | High | None | 1. `GET /api/productsList` | `responseCode` 200; non-empty `products` array; each item has `id`, `name`, `price`, `brand`, `category` |
| TC-API-010 | Products list rejects POST | negative / api | Medium | None | 1. `POST /api/productsList` | `responseCode` 405, "method is not supported" |
| TC-API-011 | Search product with a valid term | smoke / api | High | None | 1. `POST /api/searchProduct` with `search_product=top` | `responseCode` 200; non-empty `products`, each matching "top" in name or category |
| TC-API-012 | Search product with missing parameter | negative / api | High | None | 1. `POST /api/searchProduct` with no body | `responseCode` 400, "search_product parameter is missing" |
| TC-API-013 | Search product with no matching term | negative / api | Medium | None | 1. `POST /api/searchProduct` with a nonsense term | `responseCode` 200; `products` is an empty list |

## Verified quirks worth knowing

These were discovered by exercising the live site/API while building this suite (see commit
history), not assumed from the official docs. They shape several assertions above:

1. **Every API endpoint always returns HTTP 200.** The real result (`201`, `400`, `404`, `405`,
   ...) is only in the JSON `responseCode` field, never the actual HTTP status code. All API
   tests assert on `responseCode`, not `response.status_code`.
2. **`POST /api/searchProduct` matches on category as well as product name** (e.g. searching
   "top" returns a "Colour Blocked Shirt" because its category is "Tops & Shirts").
3. **The "Recommended items" carousel renders on the homepage, not `/view_cart`**, despite the
   official test case #22 documenting it on the cart page.
4. **Category links on the Products page are inside a collapsed Bootstrap accordion** — the
   group heading (Women/Men/Kids) must be expanded before a subcategory link is clickable.
5. **The site serves ad interstitials (Google Vignette) that can hijack navigation mid-test** —
   the suite blocks known ad-network requests at the Playwright context level.

## Coverage summary

- 23 UI test cases (Page Object Model, `pytest-playwright`), including 5 negative and 4
  regression cases, run across Chromium/Firefox/WebKit and under iPhone 13 emulation.
- 13 API test cases (`requests`) across 5 endpoints, positive and negative.
- Total: 36 automated test cases, comfortably over the ≥15 UI / ≥6 API bar in the project's
  definition of done.
