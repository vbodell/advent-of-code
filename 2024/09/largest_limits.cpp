#include <iostream> 
#include <limits> 

int main() {
   std::cout << "The largest int on this system is: " << std::numeric_limits<int>::max() << std::endl;
   std::cout << "The largest long on this system is: " << std::numeric_limits<long>::max() << std::endl;
   return 0;
}
