# Allure report: OFFLINE SIMULATOR, not the production backend

`allure-api-OFFLINE.zip`: static HTML report from 14 API contract tests against
a local deterministic simulator. It **does not prove** the real backend's
behavior. Real endpoint returned a connection timeout at the time of testing.

For a valid live report, restore the Stellar Burgers URL, execute
`pytest --alluredir=allure-results`, then generate Allure HTML.
Replace this offline artifact with the live report before final acceptance.
