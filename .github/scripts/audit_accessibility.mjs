#!/usr/bin/env node

import process from "node:process";

import axe from "axe-core";
import { Builder, By } from "selenium-webdriver";
import chrome from "selenium-webdriver/chrome.js";

const routes = process.argv.slice(3);
const baseUrl = process.argv[2];
if (!baseUrl || routes.length === 0 || !process.env.CHROMEDRIVER_PATH) {
  throw new Error("Usage: audit_accessibility.mjs BASE_URL ROUTE... with CHROMEDRIVER_PATH set");
}

const options = new chrome.Options().addArguments("--headless=new", "--no-sandbox", "--disable-dev-shm-usage");
const service = new chrome.ServiceBuilder(process.env.CHROMEDRIVER_PATH);
const driver = await new Builder().forBrowser("chrome").setChromeOptions(options).setChromeService(service).build();

let failed = false;

async function runAxe(label) {
  await driver.executeScript(axe.source);
  const results = await driver.executeAsyncScript(`
    const done = arguments[arguments.length - 1];
    axe.run(document).then(done).catch((error) => done({ error: String(error) }));
  `);
  if (results.error) {
    throw new Error(`${label}: ${results.error}`);
  }
  if (results.violations.length > 0) {
    failed = true;
    console.error(`\n${label}: ${results.violations.length} axe violation(s)`);
    for (const violation of results.violations) {
      console.error(`- ${violation.id}: ${violation.help}`);
      for (const node of violation.nodes) {
        console.error(`  ${node.target.join(" ")}: ${node.failureSummary}`);
      }
    }
  } else {
    console.log(`${label}: no axe violations`);
  }
}

try {
  for (const theme of ["light", "dark"]) {
    await driver.get(`${baseUrl}/`);
    await driver.executeScript("localStorage.setItem('theme', arguments[0]);", theme);
    for (const route of routes) {
      await driver.get(new URL(route, baseUrl).toString());
      await driver.wait(async () => (await driver.executeScript("return document.documentElement.dataset.theme;")) === theme, 5000);
      await driver.sleep(750);
      await runAxe(`${theme} ${route}`);

      if (route === "/") {
        const toggles = await driver.findElements(By.css(".navbar .dropdown-toggle"));
        if (toggles.length > 0 && (await toggles[0].isDisplayed())) {
          await toggles[0].click();
          await driver.sleep(200);
          await runAxe(`${theme} ${route} (open navigation menu)`);
        }
      }
    }
  }
} finally {
  await driver.quit();
}

if (failed) {
  process.exitCode = 1;
}
