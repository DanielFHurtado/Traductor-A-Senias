import 'package:flutter/material.dart';
import 'package:flutter_test/flutter_test.dart';

import 'package:flutter_application_1/main.dart';

void main() {
  testWidgets('Agregar una tarea actualiza la lista', (WidgetTester tester) async {
    await tester.pumpWidget(const TodoApp());

    // Verificar que no hay tareas al inicio
    expect(find.text('No hay tareas, ¡agrega una!'), findsOneWidget);

    // Escribir una nueva tarea
    await tester.enterText(find.byType(TextField), 'Estudiar Flutter');
    await tester.tap(find.text('Agregar'));
    await tester.pump();

    // Verificar que la tarea aparece en la lista
    expect(find.text('Estudiar Flutter'), findsOneWidget);
    expect(find.text('No hay tareas, ¡agrega una!'), findsNothing);
  });

  testWidgets('Marcar una tarea como completada', (WidgetTester tester) async {
    await tester.pumpWidget(const TodoApp());

    // Agregar una tarea
    await tester.enterText(find.byType(TextField), 'Ir al gimnasio');
    await tester.tap(find.text('Agregar'));
    await tester.pump();

    // Verificar que la tarea aparece
    expect(find.text('Ir al gimnasio'), findsOneWidget);

    // Marcar la tarea como completada (checkbox)
    await tester.tap(find.byType(Checkbox));
    await tester.pump();

    // Verificar que el checkbox está marcado
    Checkbox checkbox = tester.widget(find.byType(Checkbox));
    expect(checkbox.value, isTrue);
  });

  testWidgets('Eliminar una tarea de la lista', (WidgetTester tester) async {
    await tester.pumpWidget(const TodoApp());

    // Agregar una tarea
    await tester.enterText(find.byType(TextField), 'Comprar leche');
    await tester.tap(find.text('Agregar'));
    await tester.pump();

    expect(find.text('Comprar leche'), findsOneWidget);

    // Abrir el diálogo de eliminar
    await tester.tap(find.byIcon(Icons.delete));
    await tester.pumpAndSettle();

    // Confirmar eliminación
    await tester.tap(find.text('Eliminar'));
    await tester.pump();

    // Verificar que ya no existe
    expect(find.text('Comprar leche'), findsNothing);
  });
}

