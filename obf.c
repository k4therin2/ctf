char turing[]="\033\027\002\032\000\131\015\024\014\015\036\016\022\021\012\107\006";
char semaphore='}';char trie='{';char link_state='c';int main(int argc,char **argv){
int i;for(i=0;i<sizeof(turing)-1;i++){if(i%3==0){putchar(turing[i]^semaphore);}else
if(i%3==1){putchar(turing[i]^trie);}else{putchar(turing[i]^link_state);}}putchar('\n');}
