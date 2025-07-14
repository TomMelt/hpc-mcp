#include <vector>
#include <array>
#include <stdexcept>
#include<iostream>

class ArrayView2D {
public:
    ArrayView2D(std::vector<int> _data, std::array<int,2> shape) :
    data(_data), size_0(shape[0]), size_1(shape[1]) {
        if (_data.size() != this->size_0 * this->size_1) {
            throw std::runtime_error("Size mismatch");
        }
    }

    auto& operator()(std::size_t i, std::size_t j) {
        return this->data[j * this->size_0 + i];
    }

private:
    std::vector<int>& data;
    std::size_t size_0;
    std::size_t size_1;
};



int main() {
    std::vector<int> array_1d = {1,2,3,4,5,6};
    ArrayView2D view_2d = ArrayView2D(array_1d, {3,2});

    // Print 2nd column
    std::cout << "array=[";
    for (std::size_t i = 0; i < 3; i++) {
        std::cout << view_2d(i,1) << ",";
    }
    std::cout << "]\n";
}
