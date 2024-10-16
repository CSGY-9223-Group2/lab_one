# Contributing to [NYU - Practical Software Supply Chain Security - FA24_CS-GY_9223_1_CF04 - 2024 Fall - Lab One]

Thank you for considering contributing to [Lab One]! We value all types of contributions, whether it's fixing bugs, improving documentation, or adding new features. To maintain a secure and high-quality codebase, we ask that all contributors follow these guidelines.

## Table of Contents
- [Code of Conduct](#code-of-conduct)
- [How to Contribute](#how-to-contribute)
- [Security Best Practices](#security-best-practices)
- [Pull Request Process](#pull-request-process)
- [Reporting Security Vulnerabilities](#reporting-security-vulnerabilities)
- [Resources](#resources)

---

## Code of Conduct

Please note that this project adheres to our [Security](SECURITY.md). By participating, you agree to uphold this.

## How to Contribute

1. **Fork the repository** and create a new branch for your contribution.
2. **Submit a pull request (PR)** when your work is ready for review.
3. Ensure your PR adheres to the project's style guides and includes proper documentation.

For more details, refer to the [GitHub Docs on Forking Projects](https://docs.github.com/en/get-started/quickstart/fork-a-repo).

## Security Best Practices

To contribute securely, please follow these security-focused best practices:

### 1. Protect Your Credentials
- **Do not hardcode sensitive information** (such as API keys, tokens, or credentials) into code.
- If you're contributing configuration files, use environment variables for secret data, and never commit `.env` or other sensitive files.
  
### 2. Follow Secure Coding Practices
- Ensure that your code adheres to secure coding standards, such as:
  - **Input validation**: Always sanitize and validate user input to prevent injection attacks.
  - **Output encoding**: Properly encode data to prevent cross-site scripting (XSS) vulnerabilities.
  - **Error handling**: Avoid leaking sensitive information through verbose error messages.

### 3. Keep Dependencies Secure
- Ensure that any new dependencies you add are up-to-date and have no known vulnerabilities. Use tools like [Dependabot](https://github.com/dependabot) to track outdated dependencies.
- Before adding a new dependency, verify its source and popularity to minimize security risks from external packages.

### 4. Use HTTPS for Remote URLs
- Always use **HTTPS** links for any external URLs in your code, documentation, or dependencies to prevent man-in-the-middle attacks.

### 5. Stay Updated
- Ensure that your development environment is using the latest versions of dependencies, libraries, and security patches.
  
### 6. Least Privilege Principle
- Limit the scope of access and permissions in your code (e.g., when accessing files, databases, or services). Always apply the principle of least privilege to minimize potential damage from security issues.

## Pull Request Process

1. Before submitting your PR, ensure:
   - **Code is thoroughly tested** and passes existing tests.
   - You’ve reviewed the code for any security vulnerabilities.
   - All added features and changes have appropriate documentation.

2. In your PR, reference any relevant issues or discussions and clearly describe the purpose and changes made.

3. Each PR will go through a **code review** where maintainers or team members will review the following:
   - **Security implications** of your changes.
   - Compliance with coding standards.
   - Test coverage and CI checks.

4. After approval, your PR will be merged by one of the maintainers.

## Reporting Security Vulnerabilities

If you discover any security vulnerabilities, **do not use GitHub Issues** to report them. Instead, please follow this process:

1. Report the issue confidentially by emailing us at [ac8978@nyu.edu].
2. Include as much detail as possible about the vulnerability.
3. We will acknowledge your report, and if necessary, we will request additional details to verify the issue.

Once confirmed, we will work on a fix and notify you once it's been resolved. We appreciate your responsible disclosure!

## Resources

- [GitHub Docs: Creating a CONTRIBUTING.md File](https://docs.github.com/en/github/building-a-strong-community/setting-guidelines-for-repository-contributors)
- [OWASP Secure Coding Practices](https://owasp.org/www-project-secure-coding-practices-quick-reference-guide/)
- [GitHub Security Best Practices](https://docs.github.com/en/code-security/getting-started/securing-your-repository)
  
---

By following these guidelines, you'll help ensure that [Lab One] remains a secure, high-quality, and welcoming community.