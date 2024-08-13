from tuf import *
repository = repository_tool.load_repository("./")
private_key = import_rsa_privatekey_from_file("./private.pem")
repository.timestamp.load_signing_key(private_key)
repository.mark_dirty(['timestamp'])
repository.writeall()
repository.write('timestamp')
