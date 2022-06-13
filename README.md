# BUSINESS CARD

This project will walk you through the process of creating your very owen business card for Apple Wallet.

> ⚠️ Please note that you need access to an Apple developer account inorder to follow this guide.

The finished business card should lock something like this:

![business card in apple wallet](/docs/business-card-in-apple-wallet.png)

---

## Step 1. Start by cloning this repository.

```bash
git clone https://github.com/felixbd/business_card.git
```

---

## Step 2. Make your business card unique

Modify the jason file `BusinessCard.pass/pass.json` inorder to display your one values.

> ⚠️ Please note that every Apple Wallet card has to have a `passTypeIdentifier` and  `teamIdentifier`.
> [How to get a passTypeIdentifier and a teamIdentifier?](#appendix-i-get-a-pass-type-identifier-and-team-id)

---

## Step 3. Install the requirements:

Before we can compress and sign the `BusinessCard.pass` folder, we need to add the thumbnail image and the logo image.
Since these images need to be scaled to serve multiple Apple devices, and therefore need to follow a strict naming
convention we will use a small Python script to simplify this process.

> Before installing teh requirements it is recommended to create a virtual environment.
> ```bash
> python3 -m venv /path/to/dir/main-env && source main-env/bin/activate
> ```

Install the required python packages (for resizing images)
```bash
pip3 install -r requirements.txt
```

---

## Step 4. Add images

Simply call teh `businesscard-imager.py` python script with the parameters `-t` or `--thumbnail` and `-l` or `--logo` with full file path.

```bash
python3 businesscard-imager.py -t /home/user/images/my-thumbnail.png -i /home/user/images/my-logo.png
```

This script will auto resize the images and will write the resized images with the correct name in the `BusinessCard.pass` directory.

---

## Step 5. Signing and Compressing the Pass

#### To download your pass signing certificate, do the following:

  1. In [Certificates, Identifiers & Profiles](http://developer.apple.com/account), select Identifiers.
  2. Under Identifiers, select Pass Type IDs.
  3. Select the pass type identifier, then click Edit.
  4. If there is a certificate listed under Production Certificates, click the Download button next to it.
  If there are no certificates listed, click the Create Certificate button, then follow the instructions to create a pass signing certificate.

#### To get the `signpass` tool, do the following:

  1. Download this book’s companion file (from the [developer downloads area](https://developer.apple.com/services-account/download?path=/iOS/Wallet_Support_Materials/WalletCompanionFiles.zip)), and locate the `signpass` project.
  2. Open the project in Xcode, and build it.
  3. Right-click on the `signpass` executable (in the Products folder in Xcode) and select Show in Finder.
  4. Move the `signpass` executable to the Documents folder.

#### To sign and compress the pass, use the `signpass` tool to sign the pass package. In Terminal, run the following commands:

```bash
cd ~/Documents
```

```bash
./signpass -p BusinessCard.pass
```

These commands create a signed and compressed pass named `BusinessCard.pkpass` in the Documents folder.
If the signpass command fails, make sure you are using your correct pass type identifier and check that the `pass.json` file contains valid JSON. 

---
---

### Appendix I. Get a Pass Type Identifier and Team ID

Every pass has a pass type identifier associated with a developer account. Pass type identifiers are managed in Member Center by a team admin.
To build this pass, request and configure a pass type identifier. (You can’t use the pass type identifier that is already in the pass because it isn’t associated with your developer account.)

#### To register a pass type identifier, do the following:

  1. In [Certificates, Identifiers & Profiles](http://developer.apple.com/account), select Identifiers.
  2. Under Identifiers, select Pass Type IDs.
  3. Click the plus (+) button.
  4. Enter the description and pass type identifier, and click Submit.

#### To find your Team ID, do the following:

  1. Open Keychain Access, and select your certificate.
  2. Select File > Get Info, and find the Organizational Unit section under Details. This is your Team ID.
  3. The pass type identifier appears in the certificate under the User ID section.

>##### Note
>You can also find your Team ID by looking at your organization profile in [Member Center](https://developer.apple.com/membercenter/).

---

## Info:
- [Getting Started by Apple](https://developer.apple.com/library/archive/documentation/UserExperience/Conceptual/PassKit_PG/index.html#//apple_ref/doc/uid/TP40012195-CH1-SW1)
- [Building Your First Pass by Apple](https://developer.apple.com/library/archive/documentation/UserExperience/Conceptual/PassKit_PG/YourFirst.html#//apple_ref/doc/uid/TP40012195-CH2-SW1)
