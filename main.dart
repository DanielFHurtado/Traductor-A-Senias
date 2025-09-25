import 'package:flutter/material.dart';

void main() {
  runApp(const TodoApp());
}

class TodoApp extends StatelessWidget {
  const TodoApp({super.key});

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'Mensajes Emergentes',
      debugShowCheckedModeBanner: false,
      theme: ThemeData(
        primarySwatch: Colors.amber,
        useMaterial3: true,
        visualDensity: VisualDensity.adaptivePlatformDensity,
      ),
      home: const TodoHomePage(),
    );
  }
}

class TodoHomePage extends StatefulWidget {
  const TodoHomePage({super.key});

  @override
  _TodoHomePageState createState() => _TodoHomePageState();
}

class _TodoHomePageState extends State<TodoHomePage> {
  final List<Map<String, dynamic>> _tasks = [];
  final TextEditingController _taskController = TextEditingController();

  // ✅ Toast personalizado con animación e ícono ✔️ (texto en cursiva)
  void _showCustomToast(BuildContext context, String message) {
    final overlay = Overlay.of(context);
    final entry = OverlayEntry(
      builder: (context) => Positioned(
        bottom: 100,
        left: MediaQuery.of(context).size.width * 0.1,
        width: MediaQuery.of(context).size.width * 0.8,
        child: Material(
          color: Colors.transparent,
          child: TweenAnimationBuilder<double>(
            duration: const Duration(milliseconds: 400),
            tween: Tween(begin: 0, end: 1),
            builder: (context, value, child) => Opacity(
              opacity: value,
              child: child,
            ),
            child: Container(
              padding: const EdgeInsets.symmetric(horizontal: 16, vertical: 12),
              decoration: BoxDecoration(
                color: Colors.black87,
                borderRadius: BorderRadius.circular(12),
              ),
              child: Row(
                mainAxisSize: MainAxisSize.min,
                children: [
                  const Icon(Icons.check_circle,
                      color: Colors.greenAccent, size: 28),
                  const SizedBox(width: 10),
                  Expanded(
                    child: Text(
                      message,
                      style: const TextStyle(
                        color: Colors.white,
                        fontSize: 16,
                        fontStyle: FontStyle.italic, // ✅ cursiva
                      ),
                    ),
                  ),
                ],
              ),
            ),
          ),
        ),
      ),
    );

    overlay.insert(entry);
    Future.delayed(const Duration(seconds: 2), () => entry.remove());
  }

  // ✅ SnackBar con texto en cursiva
  void _showSnackBar(String message,
      {String? actionLabel, VoidCallback? action}) {
    final snackBar = SnackBar(
      content: Text(
        message,
        style: const TextStyle(
          fontStyle: FontStyle.italic, // ✅ cursiva
        ),
      ),
      action: actionLabel != null
          ? SnackBarAction(
              label: actionLabel,
              textColor: Colors.orange,
              onPressed: action!,
            )
          : null,
      duration: const Duration(seconds: 3),
      backgroundColor: Colors.blueGrey,
      behavior: SnackBarBehavior.floating,
      shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(8)),
    );
    ScaffoldMessenger.of(context).showSnackBar(snackBar);
  }

  // ✅ Diálogo de confirmación para eliminar
  void _showDeleteDialog(int index) {
    showDialog(
      context: context,
      builder: (BuildContext context) {
        return AlertDialog(
          title: const Row(
            children: [
              Icon(Icons.warning, color: Colors.red),
              SizedBox(width: 8),
              Text('Eliminar Tarea'),
            ],
          ),
          content: Text(
            '¿Estás seguro de eliminar la tarea "${_tasks[index]["title"]}"?',
            style: const TextStyle(fontStyle: FontStyle.italic), // ✅ cursiva
          ),
          shape:
              RoundedRectangleBorder(borderRadius: BorderRadius.circular(12)),
          actions: <Widget>[
            TextButton(
              child: const Text('Cancelar',
                  style: TextStyle(fontStyle: FontStyle.italic)), // ✅ cursiva
              onPressed: () {
                Navigator.of(context).pop();
              },
            ),
            TextButton(
              child: const Text('Eliminar',
                  style: TextStyle(
                      fontStyle: FontStyle.italic, color: Colors.red)), // ✅ cursiva
              onPressed: () {
                setState(() {
                  String removedTask = _tasks[index]["title"];
                  _tasks.removeAt(index);
                  _showSnackBar('Tarea "$removedTask" eliminada',
                      actionLabel: 'Deshacer', action: () {
                    setState(() {
                      _tasks.insert(
                          index, {"title": removedTask, "done": false});
                    });
                  });
                });
                Navigator.of(context).pop();
              },
            ),
          ],
        );
      },
    );
  }

  // ✅ Ventana de edición en el centro
  void _showEditDialog(int index) {
    _taskController.text = _tasks[index]["title"];

    showDialog(
      context: context,
      barrierDismissible: false,
      builder: (BuildContext context) {
        return AlertDialog(
          shape:
              RoundedRectangleBorder(borderRadius: BorderRadius.circular(12)),
          backgroundColor: Colors.teal.shade50,
          title: const Text(
            'Editar Tarea',
            style: TextStyle(
                fontSize: 20,
                fontWeight: FontWeight.bold,
                fontStyle: FontStyle.italic), // ✅ cursiva
            textAlign: TextAlign.center,
          ),
          content: TextField(
            controller: _taskController,
            decoration: const InputDecoration(
              labelText: 'Nombre de la tarea',
              border: OutlineInputBorder(),
            ),
          ),
          actionsAlignment: MainAxisAlignment.spaceBetween,
          actions: [
            TextButton(
              onPressed: () => _taskController.clear(),
              child: const Text('Limpiar',
                  style: TextStyle(fontStyle: FontStyle.italic)), // ✅ cursiva
            ),
            TextButton(
              onPressed: () => Navigator.pop(context),
              child: const Text('Cancelar',
                  style: TextStyle(fontStyle: FontStyle.italic)), // ✅ cursiva
            ),
            ElevatedButton(
              onPressed: () {
                if (_taskController.text.isNotEmpty) {
                  setState(() {
                    _tasks[index]["title"] = _taskController.text;
                  });
                  _showCustomToast(
                      context, 'Tarea actualizada correctamente');
                  Navigator.pop(context);
                  _taskController.clear();
                } else {
                  _showCustomToast(
                      context, '⚠️ Por favor, ingresa un nombre de tarea');
                }
              },
              child: const Text('Guardar',
                  style: TextStyle(fontStyle: FontStyle.italic)), // ✅ cursiva
            ),
          ],
        );
      },
    );
  }

  // ✅ Agregar nueva tarea
  void _addTask() {
    if (_taskController.text.isNotEmpty) {
      setState(() {
        _tasks.add({"title": _taskController.text, "done": false});
        _showCustomToast(context, 'Tarea "${_taskController.text}" agregada');
        _taskController.clear();
      });
    } else {
      _showCustomToast(context, '⚠️ Por favor, ingresa un nombre de tarea');
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: Text('Lista de Tareas (${_tasks.length})',
            style: const TextStyle(fontStyle: FontStyle.italic)), // ✅ cursiva
        centerTitle: true,
      ),
      body: Column(
        children: [
          Padding(
            padding: const EdgeInsets.all(16.0),
            child: Row(
              children: [
                Expanded(
                  child: TextField(
                    controller: _taskController,
                    decoration: const InputDecoration(
                      labelText: 'Nueva tarea',
                      border: OutlineInputBorder(),
                    ),
                  ),
                ),
                const SizedBox(width: 8),
                ElevatedButton(
                  onPressed: _addTask,
                  child: const Text('Agregar',
                      style: TextStyle(fontStyle: FontStyle.italic)), // ✅ cursiva
                ),
              ],
            ),
          ),
          Expanded(
            child: _tasks.isEmpty
                ? const Center(
                    child: Text('No hay tareas, ¡agrega una!',
                        style: TextStyle(fontStyle: FontStyle.italic)), // ✅ cursiva
                  )
                : ListView.builder(
                    itemCount: _tasks.length,
                    itemBuilder: (context, index) {
                      return ListTile(
                        leading: Checkbox(
                          value: _tasks[index]["done"],
                          onChanged: (bool? value) {
                            setState(() {
                              _tasks[index]["done"] = value ?? false;
                            });
                          },
                        ),
                        title: Text(
                          _tasks[index]["title"],
                          style: TextStyle(
                            fontStyle: FontStyle.italic, // ✅ cursiva
                            decoration: _tasks[index]["done"]
                                ? TextDecoration.lineThrough
                                : null,
                          ),
                        ),
                        trailing: Row(
                          mainAxisSize: MainAxisSize.min,
                          children: [
                            IconButton(
                              icon:
                                  const Icon(Icons.edit, color: Colors.blue),
                              onPressed: () => _showEditDialog(index),
                            ),
                            IconButton(
                              icon:
                                  const Icon(Icons.delete, color: Colors.red),
                              onPressed: () => _showDeleteDialog(index),
                            ),
                          ],
                        ),
                      );
                    },
                  ),
          ),
        ],
      ),
    );
  }

  @override
  void dispose() {
    _taskController.dispose();
    super.dispose();
  }
}
