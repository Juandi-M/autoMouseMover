# Auto Mouse Mover - .pkg Package Generation

![Python Version](https://img.shields.io/badge/python-3.x-blue)
![macOS](https://img.shields.io/badge/platform-macOS-lightgrey)
![License](https://img.shields.io/badge/license-Commercial-red)

This document provides a step-by-step guide to generate the `.pkg` packages needed to distribute the Auto Mouse Mover application.

## Prerequisites

Before you begin, make sure you have the following components installed:

- **Python 3:** Ensure you have Python 3 installed on your system.
- **Py2app:** A tool to convert Python scripts into standalone Mac OS X applications.
  ```bash
  pip install py2app
  ```
- **pkgbuild and productbuild:** Command-line tools provided by Apple for creating installer packages. These are typically included with Xcode or the Command Line Tools for Xcode.

## Directory Structure

Your project directory should have the following structure:

```bash
package/
├── welcome.txt
├── LICENSE.txt
├── README.MD
├── background.png
└── distribution.xml
```

## Purpose of Each File in the Package

- **welcome.txt:** Contains the welcome message displayed at the beginning of the installation process.
- **LICENSE.txt:** Contains the license agreement that the user must accept to proceed with the installation.
- **background.png:** The background image displayed during the installation process.
- **distribution.xml:** Defines the structure and behavior of the installer package.

## Purpose of setup.py

The `setup.py` script is used by py2app to package the Python application into a standalone macOS application. It specifies the main script, data files, and options for the application.

## Steps to Generate the .pkg Packages

1. **Generate the Standalone Application**
   Run py2app to create the standalone application:

   ```bash
   cd mac
   python3 setup.py py2app
   ```

   This will create the application in the `dist` directory.

2. **Create the Application Package**
   Use `pkgbuild` to create a package for the application:

   ```bash
   pkgbuild --root dist/AutoMouseMover.app --identifier com.automousemover --version 0.1.0 --install-location /Applications ../AutoMouseMover.pkg
   ```

3. **Create the Installer Package**
   Use `productbuild` to create the final installer package that includes the application package and provides a user-friendly installation interface:

   ```bash
   cd mac
   productbuild --distribution package/distribution.xml --package-path ../AutoMouseMover.pkg --resources package --version 0.1.0 ../AutoMouseMoverInstaller.pkg
   ```

## Explanation of Generated .pkg Files

- **AutoMouseMover.pkg:** This package contains all the files necessary for the application. It is an internal component and is not distributed directly to users.
- **AutoMouseMoverInstaller.pkg:** This is the installer package that wraps `AutoMouseMover.pkg` and provides a graphical installation interface. This is the file you distribute to users for installing the application.

## Summary

- Generate the standalone application using `py2app`.
- Create the application package using `pkgbuild`.
- Create the installer package using `productbuild`.

By following these steps, you can generate the `.pkg` packages needed to distribute the Auto Mouse Mover application to users.
