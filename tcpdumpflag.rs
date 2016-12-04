use std::net::{TcpListener, TcpStream};
use std::io::{Read, Write};
use std::time::Duration;


fn handle_client(mut stream: TcpStream) {
    let _ = stream.set_read_timeout(Some(Duration::new(1, 0)));
    let mut b: [u8; 16] = [0; 16];
    let r = stream.read(&mut b);
    match r {
        Ok(n) => {
            if n != 0 {
                return;
            }
        }
        Err(_) => {}
    }
    let response = "flag{All men are created equal}\n";
    let _ = stream.write(response.as_bytes());
}

fn main() {
    let listener = TcpListener::bind("0.0.0.0:1776").unwrap();

    for stream in listener.incoming() {
        match stream {
            Ok(stream) => {
                handle_client(stream);
            }
            Err(_) => {}
        }
    }
}
