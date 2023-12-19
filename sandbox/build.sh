cd /home/test/web-compiler-server/sandbox/
sudo cargo build --release
sudo rm -rf /usr/bin/sandbox 
sudo cp target/release/sandbox /usr/bin/