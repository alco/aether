#include <math.h>
#include <functional>
#include <initializer_list>


template<typename T, unsigned N>
// T: Numeric(Add,Sub,Mul,Div,Mod,...)
// N: Integral > 0
struct Vector {
    // Construction

    Vector(std::initializer_list<T> list) {
        int i = 0;
        for (const T& x: list) {
            v[i++] = x;
        }
    }

    Vector(const Vector<T, N>& other) { // clone constructor
        memcpy(v, other.v, sizeof(v));
    }


    // Immutable ops

    T len() const {
        return sqrt(len2());
    }

    T len2() const {
        // NOTE: vectorizable
        T result = 0;
        for (int i = 0; i < N; ++i) {
            result += v[i] * v[i];
        }
        return result;
    }

    T dot(const Vector<T, N>& other) const {
        T result = 0;
        for (int i = 0; i < N; ++i) {
            result += v[i] * other.v[i];
        }
        return result;
    }

    void print() const {
        printf("(");
        for (int i = 0; i < N; ++i) {
            printf("%d", v[i]);
            if (i < N-1) {
                printf(" ");
            }
        }
        printf(")\n");
    }

    // Unary

    Vector& neg() {
        for (int i = 0; i < N; ++i) {
            v[i] = -v[i];
        }
        return *this;
    }

    // Binary (scalar)

    Vector& scale(T scalar) {
        for (int i = 0; i < N; ++i) {
            v[i] *= scalar;
        }
        return *this;
    }

    // Binary (vector)

    Vector& add(const Vector<T, N>& other) {
        for (int i = 0; i < N; ++i) {
            v[i] += other.v[i];
        }
        return *this;
    }

    Vector& sub(const Vector<T, N>& other) {
        for (int i = 0; i < N; ++i) {
            v[i] -= other.v[i];
        }
        return *this;
    }

    Vector& mul(const Vector<T, N>& other) {
        // per-component multiplication
        for (int i = 0; i < N; ++i) {
            v[i] *= other.v[i];
        }
        return *this;
    }

    Vector& div(const Vector<T, N>& other) {
        // per-component division
        for (int i = 0; i < N; ++i) {
            v[i] /= other.v[i];
        }
        return *this;
    }

    // Misc

    Vector& map(std::function<T(const T&)> f) {
        for (int i = 0; i < N; ++i) {
            v[i] = f(v[i]);
        }
        return *this;
    }

    // Layout

    T v[N];
};

#if 0

let a = vector{1, 2, 3}
let b = vector{-3, -2, -1}

f = i -> i^2

// in a naive implementation, the following expression would
// produce 6 temporaries
let prod = ((a + 2 * b) * (2 * a - b)) • f×a
print(prod)

// ^^^ the above results in the following generated code ^^^

#endif

typedef int Num;

void test1() {
    const auto a = Vector<Num, 3>{1, 2, 3};
    const auto b = Vector<Num, 3>{-3, -2, -1};

    auto f = [](Num i) { return i * i; };

    // Assume add is commutative
    auto v_tmp = Vector<Num, 3>(b).scale(2).add(a);  // +1

    // Assume mul is commutative
    auto v = Vector<Num, 3>(a).scale(2).sub(b).mul(v_tmp); // +1

    // v_tmp can be rebound now
    v_tmp = Vector<Num, 3>(a).map(f); // +1

    // Assume dot is commutative
    auto prod = v.dot(v_tmp);

    // 3 temporaries

    printf("%d\n", prod);
}

#if 0

let a = vector{1, 2, 3}
let b = vector{-3, -2, -1}

f = i -> i^2

// 10 temporaries
let c = (4*a - 2*b) * f×a + (3*b - 5*a*a*b)
print(c)

// ^^^ the above results in the following generated code ^^^

#endif

void test2() {
    const auto a = Vector<Num, 3>{1, 2, 3};
    const auto b = Vector<Num, 3>{-3, -2, -1};

    auto f = [](Num i) { return i * i; };

    auto b_tmp = Vector<Num, 3>(b).scale(2);            // +1
    auto v_tmp = Vector<Num, 3>(a).scale(4).sub(b_tmp); // +1

    auto a_mapped = Vector<Num, 3>(a).map(f);  // +1
    v_tmp.mul(a_mapped);

    // Assume 3*b = 2*b + 1
    b_tmp.add(b);

    auto a_tmp = Vector<Num, 3>(a).mul(a).mul(b).scale(5); // +1
    b_tmp.sub(a_tmp);

    v_tmp.add(b_tmp); // rename to c to get the result
    v_tmp.print();

    // 4 temporaries
}


int main(int argc, const char *argv[])
{
    test1();
    test2();
    return 0;
}
