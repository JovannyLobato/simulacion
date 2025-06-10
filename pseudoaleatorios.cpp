#include <iostream>
#include <string>
#include <iomanip>
using namespace std;

// cuadrados medios (falta validacion de semilla mayor a 3 cifras)
// productos medios (chequear validaciones)
// multiplicador constantea
// 
// puede elegir varias pruebas
// tres opciones de nivel de confianza
// por default 95% de confianza
// prueba de media
// 	regresa lim. Inf y lim. Sup.
// prueba de varianza 
// prueba de uniformidada
// 	valor chi y valor chi en tablas

void multiplicadorConst(int x, int c, int n) {
    string sxi;

    //string::size_type sz;
    double sz;
    double xi = 0;
    double xa = x;

    for (int i = 0; i < n; i++) {
        xi = xa * c;
        cout << fixed << setprecision(0) << i + 1 << '\t' << xi << '\t';

        sxi = to_string((long long)xi);
        if (sxi.length() % 2 != 0) {
            sxi = "0" + sxi;
        }
        while (sxi.length() < 8) {
            sxi = "0" + sxi;
        }

        int inicio = (sxi.length() - 4) / 2;
        string centro = sxi.substr(inicio, 4);

        xa = stoi(centro);
        cout << fixed << setprecision(4) << (xa / 10000.0) << endl;
    }
}

void productosMedios() {
    int x0, x1, cantidad;
    while (true) {
        cout << "ingresa la primer y segunda semilla" << endl;
        cin >> x0 >> x1;
        if (x0 > 1000 || x1 > 1000) {
            break;
        }
        cout << "Las semillas ingresadas son inválidas" << endl;
    }
    while (true) {
        cout << "Ingresa el numero de numeros aleatorios que quieres";
        cin >> cantidad;
        if (cantidad >= 1) {
            break;
        }
    }

    int conta = 2;
    int r = 1;
    int y = 0;

    while (cantidad >= 1) {
        int producto = x0 * x1;

        // Convertir el producto a string
        ostringstream oss;
        oss << producto;
        string c = oss.str();

        if (c.length() % 2 != 0) {
            c = "0" + c;
        }

        int inicio = (c.length() - 4) / 2;
        string centro = c.substr(inicio, 4);

        int nuevoNumero = stoi(centro);
        double ri = nuevoNumero / 10000.0;

        cout << "y" << y << "= " << x0 << "\t"
             << x1 << "\t" << producto << "\t  "
             << "x" << conta << "= " << nuevoNumero << "\t"
             << "r" << r << "= " << ri << endl;

        x0 = x1;
        x1 = nuevoNumero;

        conta++;
        r++;
        cantidad--;
        y++;
    }
}

void cuadradosMedios(int x0, int cantidad) {
    if (x0 < 1000) {
        cout << "La semilla ingresada es inválida (mínimo 4 dígitos)" << endl;
        return;
    }

    for (int i = 0; i < cantidad; i++) {
        int producto = x0 * x0;
        string c = to_string(producto);

        if (c.length() % 2 != 0) {
            c = "0" + c;
        }
        while (c.length() < 8) {
            c = "0" + c;
        }

        int inicio = (c.length() - 4) / 2;
        string centro = c.substr(inicio, 4);

        x0 = stoi(centro);
        double ri = x0 / 10000.0;

        cout << i + 1 << "\t" << producto << "\t" << x0 << "\t" << ri << endl;
    }
}



int main() {
    int o = -4;

    while (true) {
        cout << "opciones" << endl;
        cout << "(1) Cuadrados medios" << endl;
        cout << "(2) Productos medios" << endl;
        cout << "(3) multiplicador constante" << endl;
        cout << "(0) salir" << endl;
        cin >> o;
        if (o == 1 || o == 2 || o == 3 || o == 0) {
            break;
        }
    }

    if (o == 0) return 0;

    if (o == 1) {
        int semilla, cantidad;
        cout << "Ingresa la semilla (mínimo 4 dígitos): ";
        cin >> semilla;

        cout << "Cantidad de números pseudoaleatorios a generar: ";
        cin >> cantidad;

        cuadradosMedios(semilla, cantidad);
    }

    if (o == 2) {
        productosMedios();
    }

    int x, c, i;
    if (o == 3) {
        cout << "Ingresa la semilla, la constante y la cantidad de numeros pseudoaleatorios que quieres" << endl;
        while (cin >> x >> c >> i) {
            if (x > 999 && x < 10000 && c > 99 && c < 10000) {
                break;
            }
            cout << "x y c deben de ser de exactamente 4 dígitos" << endl;
        }
        multiplicadorConst(x, c, i);
    }

    return 0;
}

