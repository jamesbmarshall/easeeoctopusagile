# Automatic Easee Site Charging Price Updater for Octopus Agile

This code will automatically take the current half-hourly price from Octopus for their Agile tariff and set it as the site charging price for your Easee electric vehicle charger. There are two methods included: an HTML and JS file, and as a Python Azure Function on a timer.

### Background

Octopus publish half-hourly pricing for their Agile tariff. It's therefore important to know the current price so you can more accurately understand how much a charging session costs when using your Easee wall charger. Without automation, you would have to manually update the price or set a general rate. This code seeks to automate that process reliably, so that you will always see the current price reflected in the app.

## Hosting

I run this in Azure using Azure Functions. If you don't want to do that, you'll need to find some way of hosting the code and scheduling it to run every 30 minutes. Azure Functions are a low cost option, but not free, and will require you to set up a subscription if you don't have one. If you have access to other means (such as your own server, etc.) you may find it easier to take the code and modify it for your environment.

The HTML file is included so that you can run it on a web server and trigger it manually. I started off writing it that way before deciding to switch to Python.

# Configuration

As I iterate on this project, I'll try to make it easier to configure. For now, you'll have to put up with my shocking lack of commenting and good practice and do a bit of reading.

## General

You will need to log into the [Octopus developer portal](https://octopus.energy/dashboard/new/accounts/personal-details/api-access) with your account credentials. On there, you'll find an example of the URL you'll need to include in the code. Pay particular attention to the region suffix, as this may be different where you live. In my configuration it ends in H (E-1R-AGILE-FLEX-22-11-25-H), if yours is different, update the code accordingly.

The rest of the URL should be the same, and if it changes, I'll update this project ASAP.

## HTML Version

There are three things you'll need to change:

- \*\*\*YOURUSERNAME\*\*\* - this is your Easee account username, most likely an email address.
- \*\*\*YOURPASSWORD\*\*\* - this is your Easee account password.
- \*\*\*YOURSITEID\*\*\* - this is your Easee site ID. If you log into the Easee cloud portal, you can find this in the URL. It's a number.

Since these are unique and sensitive pieces of information, I strongly recommend caution in choosing where to host the file. Anyone will be able to inspect the source and see this information.

## Python / Azure Function

Since functions support enviornment variables, or application settings, which are managed under the configuration section for your application, we can use these to securely store info and keep the rest of the source code clean. You'll need to create three application settings:

- EASEE_USER, for your Easee account username.
- EASEE_PASSWORD, for your Easee account password.
- EASEE_SITE_ID, for your Easee site ID.

If you populate those settings with your details, you shouldn't need to make any further changes _unless_ you need to edit the Octopus URL. I created and managed the function using VS Code, which makes it easy to edit and deploy. Since the function includes other libraries you'll need to use this method as I don't think you can do it all via the portal.

Good luck!
