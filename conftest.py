import pytest
import allure

@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """
    This hook is triggered after each test.
    If the test failed, it will capture a screenshot (for UI tests with driver).
    """
    outcome = yield
    result = outcome.get_result()

    if result.when == "call" and result.failed:
        # Get the driver from the test (if available)
        driver = getattr(item.instance, "driver", None)
        if driver:
            screenshot_path = f"screenshot_{item.name}.png"
            driver.save_screenshot(screenshot_path)
            with open(screenshot_path, "rb") as f:
                allure.attach(
                    f.read(),
                    name=f"{item.name}_screenshot",
                    attachment_type=allure.attachment_type.PNG
                )
