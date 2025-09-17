import 'dart:io';
import 'package:flutter/material.dart';
import 'package:shared_preferences/shared_preferences.dart';
import 'package:path_provider/path_provider.dart';
import 'package:share_plus/share_plus.dart';

void main() {
  runApp(const MiAplicacion());
}

class MiAplicacion extends StatelessWidget {
  const MiAplicacion({super.key});

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'Aplicación de Formulario',
      debugShowCheckedModeBanner: false,
      theme: ThemeData(primarySwatch: Colors.blue),
      home: const PantallaFormulario(),
      routes: {
        '/lista': (context) => const PantallaLista(),
      },
    );
  }
}

class PantallaFormulario extends StatefulWidget {
  const PantallaFormulario({super.key});

  @override
  State<PantallaFormulario> createState() => _PantallaFormularioState();
}

class _PantallaFormularioState extends State<PantallaFormulario> {
  final _formKey = GlobalKey<FormState>();
  final _nombreController = TextEditingController();
  final _telefonoController = TextEditingController();

  Future<void> _guardarContacto(String nombre, String telefono) async {
    final prefs = await SharedPreferences.getInstance();
    List<String> contactos = prefs.getStringList('contactos') ?? [];
    contactos.add("$nombre: $telefono");
    await prefs.setStringList('contactos', contactos);
    if (mounted) {
      ScaffoldMessenger.of(context).showSnackBar(
        const SnackBar(content: Text('Contacto guardado')),
      );
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text('Formulario')),
      body: Padding(
        padding: const EdgeInsets.all(16.0),
        child: Form(
          key: _formKey,
          child: Column(
            children: [
              TextFormField(
                controller: _nombreController,
                decoration: const InputDecoration(
                  labelText: 'Ingresa tu nombre',
                  border: OutlineInputBorder(),
                ),
                validator: (value) =>
                    value == null || value.isEmpty ? 'Por favor, ingresa un nombre' : null,
              ),
              const SizedBox(height: 10),
              TextFormField(
                controller: _telefonoController,
                decoration: const InputDecoration(
                  labelText: 'Ingresa tu teléfono',
                  border: OutlineInputBorder(),
                ),
                validator: (value) =>
                    value == null || value.isEmpty ? 'Por favor, ingresa un teléfono' : null,
              ),
              const SizedBox(height: 20),
              ElevatedButton(
                onPressed: () {
                  if (_formKey.currentState!.validate()) {
                    _guardarContacto(_nombreController.text, _telefonoController.text);
                    _nombreController.clear();
                    _telefonoController.clear();
                  }
                },
                child: const Text('Guardar Contacto'),
              ),
              const SizedBox(height: 20),
              ElevatedButton(
                onPressed: () {
                  Navigator.pushNamed(context, '/lista');
                },
                child: const Text('Ver Lista de Contactos'),
              ),
            ],
          ),
        ),
      ),
    );
  }

  @override
  void dispose() {
    _nombreController.dispose();
    _telefonoController.dispose();
    super.dispose();
  }
}

class PantallaLista extends StatefulWidget {
  const PantallaLista({super.key});

  @override
  State<PantallaLista> createState() => _PantallaListaState();
}

class _PantallaListaState extends State<PantallaLista> {
  List<String> _contactos = [];
  List<String> _filtrados = [];
  final _searchController = TextEditingController();

  @override
  void initState() {
    super.initState();
    _cargarContactos();
    _searchController.addListener(_filtrarContactos);
  }

  Future<void> _cargarContactos() async {
    final prefs = await SharedPreferences.getInstance();
    final contactos = prefs.getStringList('contactos') ?? [];
    setState(() {
      _contactos = contactos;
      _filtrados = contactos;
    });
  }

  void _filtrarContactos() {
    String query = _searchController.text.toLowerCase();
    setState(() {
      _filtrados = _contactos
          .where((c) => c.toLowerCase().contains(query))
          .toList();
    });
  }

  Future<void> _eliminarContacto(int index) async {
    final prefs = await SharedPreferences.getInstance();
    _contactos.removeAt(index);
    await prefs.setStringList('contactos', _contactos);
    _filtrarContactos();
  }

  /// 🔹 Exportar contactos en CSV y guardar en TXT
  Future<void> _exportarContactos() async {
    if (_contactos.isEmpty) {
      if (mounted) {
        ScaffoldMessenger.of(context).showSnackBar(
          const SnackBar(content: Text('No hay contactos para exportar')),
        );
      }
      return;
    }

    // Crear CSV
    final csvData = StringBuffer();
    csvData.writeln("Nombre,Teléfono");
    for (var contacto in _contactos) {
      final partes = contacto.split(":");
      final nombre = partes[0].trim();
      final telefono = partes.length > 1 ? partes[1].trim() : "";
      csvData.writeln("$nombre,$telefono");
    }

    // 📌 Guardar copia fija en TXT (en documentos del dispositivo)
    final docsDir = await getApplicationDocumentsDirectory();
    final txtFile = File('${docsDir.path}/contactos_guardados.txt');
    await txtFile.writeAsString(_contactos.join('\n'));

    // 📌 Guardar CSV temporal para compartir
    final tempDir = await getTemporaryDirectory();
    final csvFile = File('${tempDir.path}/contactos.csv');
    await csvFile.writeAsString(csvData.toString());

    await Share.shareXFiles(
      [XFile(csvFile.path, mimeType: 'text/csv')],
      text: 'Lista de contactos en CSV',
    );

    if (mounted) {
      ScaffoldMessenger.of(context).showSnackBar(
        SnackBar(content: Text('Contactos guardados en: ${txtFile.path}')),
      );
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('Lista de Contactos'),
        actions: [
          IconButton(
            icon: const Icon(Icons.share),
            onPressed: _exportarContactos,
          )
        ],
      ),
      body: Column(
        children: [
          Padding(
            padding: const EdgeInsets.all(8.0),
            child: TextField(
              controller: _searchController,
              decoration: const InputDecoration(
                labelText: 'Buscar contacto',
                border: OutlineInputBorder(),
                prefixIcon: Icon(Icons.search),
              ),
            ),
          ),
          const Padding(
            padding: EdgeInsets.symmetric(vertical: 8.0),
            child: Text(
              '👉 Desliza hacia la izquierda sobre un contacto para eliminarlo',
              style: TextStyle(fontSize: 14, fontWeight: FontWeight.w500, color: Colors.grey),
            ),
          ),
          Expanded(
            child: _filtrados.isEmpty
                ? const Center(child: Text('No hay contactos guardados'))
                : ListView.builder(
                    itemCount: _filtrados.length,
                    itemBuilder: (context, index) {
                      return Dismissible(
                        key: Key(_filtrados[index]),
                        direction: DismissDirection.endToStart,
                        onDismissed: (direction) {
                          int realIndex = _contactos.indexOf(_filtrados[index]);
                          _eliminarContacto(realIndex);
                          ScaffoldMessenger.of(context).showSnackBar(
                            const SnackBar(content: Text('Contacto eliminado')),
                          );
                        },
                        background: Container(
                          color: Colors.red,
                          alignment: Alignment.centerRight,
                          padding: const EdgeInsets.symmetric(horizontal: 20),
                          child: const Icon(Icons.delete, color: Colors.white),
                        ),
                        child: ListTile(
                          title: Text(_filtrados[index]),
                        ),
                      );
                    },
                  ),
          ),
        ],
      ),
      floatingActionButton: FloatingActionButton(
        onPressed: () => Navigator.pop(context),
        child: const Icon(Icons.arrow_back),
      ),
    );
  }

  @override
  void dispose() {
    _searchController.dispose();
    super.dispose();
  }
}
