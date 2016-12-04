use std::net::{TcpListener, TcpStream};
use std::io::Write;


fn handle_client(mut stream: TcpStream) {
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
