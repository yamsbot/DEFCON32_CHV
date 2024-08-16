# DEFCON32 CHV (TUF)
will update readme later.

## Setup
Host "TUF" web server locally, in this case on port 8003. The TUF web server will contain metadata, which is a symbolic link to the current directory, which contains the forged
- timestamp.json
- snapshot.json
- targets.json

targets.json will contain a listing for the malicious software to be executed, in this case, tcmupdate_v0.2.0.py. Once the victim TUF server hits our malicious TUF server, the cached version of timestamp.json will be outdated, thus pulling in all of our malicious metadata and executing the malicious firmware. 

## Flag 1
Connecting to the TUF server update CLI we are greeted with a prompt asking users to "Enter type name:" which will then download and execute the file that matches the regex query.\

The following files are available:
- 870cba60f57b8cbee2647241760d9a89f3c91dba2664467694d7f7e4e6ffaca588f8453302f196228b426df44c01524d5c5adeb2f82c37f51bb8c38e9b0cc900.tcmupdate_v0.2.0.py
- 9bbef34716da8edb86011be43aa1d6ca9f9ed519442c617d88a290c1ef8d11156804dcd3e3f26c81e4c14891e1230eb505831603b75e7c43e6071e2f07de6d1a.tcmupdate_v0.2.0.py
- 481997bcdcdf22586bc4512ccf78954066c4ede565b886d9a63c2c66e2873c84640689612b71c32188149b5d6495bcecbf7f0d726f5234e67e8834bb5b330872.tcmupdate_v0.3.0.py
- bc7e3e0a6ec78a2e70e70f87fbecf8a2ee4b484ce2190535c045aea48099ba218e5a968fb11b43b9fcc51de5955565a06fd043a83069e6b8f9a66654afe6ea57.tcmupdate_v0.4.0.py

The CLI program tries to stop users from "rolling-back" the software by checking:
```python3
if "." in name:
    print("Not allowed!")
    return
```
Since the input is parsed as regex, we can easily bypass this filter and rollback to version v0.3.0 by using the following regex:
`tcmupdate_v0[\D]3`
Once v0.3.0 is executed we are greeted with the first flag and on our way to obtaining the second flag. Obtaining the second flag is more tricky, this is because we have to supply the program with the URL of a TUF server, which will then validate that the metadata objects on the remote TUF server have been signed, then download and execute the program specified from the remote server. 

## Flag 2
Inside of the supplied `root.json` file we see that 3 of the 4 metadata files in use are signed by the same private key, and the public key that matches the keyid is supplied to us:
```json
"f1f66ca394996ea67ac7855f484d9871c8fd74e687ebab826dbaedf3b9296d14" : {
            "keyid_hash_algorithms" : [
               "sha256",
               "sha512"
            ],
            "keytype" : "rsa",
            "keyval" : {
               "public" : "-----BEGIN PUBLIC KEY-----\nMIHyMA0GCSqGSIb3DQEBAQUAA4HgADCB3AKB1EisCnVT27PEvEllOdXcRW5GhuJu\nHci8ZJAOeJzd7Q6vX99lmMOeEEVECvmDexLxyqpvy/qbYrm/sJLftrSJXviwCjNE\nDx6vNpeLza1EefWTpVlLCJ4LD0/Ts3Y7OJ8ZHoEfWSa8lMa8+uSc+IXCAeLOHTb6\nBlpf2mBbcPjXWFVGCS9RviidPkBcR9vwa74x5jK+lAijvxmR8spfJvPz/fC2/2F3\nu9RgDYKBwPvfU59b9ObRDgAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAADsGGj\nAgMBAAE=\n-----END PUBLIC KEY-----\n"
            },
            "scheme" : "rsassa-pss-sha256"
         }
      },
      "roles" : {
         "root" : {
            "keyids" : [
               "37eecb4fe22b7342995d648c31625634d4fb53090b91f256071ff4a0ee7e4870"
            ],
            "threshold" : 1
         },
         "snapshot" : {
            "keyids" : [
               "f1f66ca394996ea67ac7855f484d9871c8fd74e687ebab826dbaedf3b9296d14"
            ],
            "threshold" : 1
         },
         "targets" : {
            "keyids" : [
               "f1f66ca394996ea67ac7855f484d9871c8fd74e687ebab826dbaedf3b9296d14"
            ],
            "threshold" : 1
         },
         "timestamp" : {
            "keyids" : [
               "f1f66ca394996ea67ac7855f484d9871c8fd74e687ebab826dbaedf3b9296d14"
            ],
            "threshold" : 1
         }
      },
      "spec_version" : "1.0",
      "version" : 1
   }
}
```

The public key being:
```
-----BEGIN PUBLIC KEY-----
MIHyMA0GCSqGSIb3DQEBAQUAA4HgADCB3AKB1EisCnVT27PEvEllOdXcRW5GhuJu
Hci8ZJAOeJzd7Q6vX99lmMOeEEVECvmDexLxyqpvy/qbYrm/sJLftrSJXviwCjNE
Dx6vNpeLza1EefWTpVlLCJ4LD0/Ts3Y7OJ8ZHoEfWSa8lMa8+uSc+IXCAeLOHTb6
Blpf2mBbcPjXWFVGCS9RviidPkBcR9vwa74x5jK+lAijvxmR8spfJvPz/fC2/2F3
u9RgDYKBwPvfU59b9ObRDgAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAADsGGj
AgMBAAE=
-----END PUBLIC KEY-----
```
Supplying this public key to the [RsaCtfTool](https://github.com/RsaCtfTool/RsaCtfTool) we are able to use the "Lehman attack" (?) to extract the private key from the public key. With the private key we are able to forge and sign our own metadata objects and supply our own malicious "firmware updates"

This attack is programmatically carried out in solve.py and sign.py
