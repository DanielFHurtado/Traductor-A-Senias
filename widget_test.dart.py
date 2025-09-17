import 'package:flutter/material.dart';
import 'package:flutter_test/flutter_test.dart';
import 'package:ejercicio2/main.dart';

void main() {
  testWidgets('Formulario carga correctamente con campos de nombre y teléfono', (WidgetTester tester) async {
    // Renderiza la app
    await tester.pumpWidget(const MiAplicacion());

    // Verifica que el AppBar de la pantalla principal tenga el título correcto
    expect(find.text('Formulario'), findsOneWidget);

    // Verifica que existan los campos de texto para nombre y teléfono
    expect(find.widgetWithText(TextFormField, 'Ingresa tu nombre'), findsOneWidget);
    expect(find.widgetWithText(TextFormField, 'Ingresa tu teléfono'), findsOneWidget);

    // Verifica que existan los botones principales
    expect(find.widgetWithText(ElevatedButton, 'Guardar Contacto'), findsOneWidget);
    expect(find.widgetWithText(ElevatedButton, 'Ver Lista de Contactos'), findsOneWidget);
  });

  testWidgets('Navegación a la lista de contactos', (WidgetTester tester) async {
    await tester.pumpWidget(const MiAplicacion());

    // Navegar a la lista
    await tester.tap(find.widgetWithText(ElevatedButton, 'Ver Lista de Contactos'));
    await tester.pumpAndSettle();

    // Verifica que la pantalla cargue
    expect(find.text('Lista de Contactos'), findsOneWidget);
    expect(find.text('No hay contactos guardados'), findsOneWidget);
  });

  testWidgets('Guardar y mostrar contacto en la lista', (WidgetTester tester) async {
    await tester.pumpWidget(const MiAplicacion());

    // Ingresar nombre y teléfono
    await tester.enterText(find.widgetWithText(TextFormField, 'Ingresa tu nombre'), 'Juan');
    await tester.enterText(find.widgetWithText(TextFormField, 'Ingresa tu teléfono'), '123456789');

    // Guardar contacto
    await tester.tap(find.widgetWithText(ElevatedButton, 'Guardar Contacto'));
    await tester.pumpAndSettle();

    // Navegar a lista
    await tester.tap(find.widgetWithText(ElevatedButton, 'Ver Lista de Contactos'));
    await tester.pumpAndSettle();

    // Verifica que el contacto aparezca con nombre y teléfono
    expect(find.text('Juan: 123456789'), findsOneWidget);
  });

  testWidgets('Buscar contacto en la lista', (WidgetTester tester) async {
    await tester.pumpWidget(const MiAplicacion());

    // Guardar un contacto
    await tester.enterText(find.widgetWithText(TextFormField, 'Ingresa tu nombre'), 'Maria');
    await tester.enterText(find.widgetWithText(TextFormField, 'Ingresa tu teléfono'), '987654321');
    await tester.tap(find.widgetWithText(ElevatedButton, 'Guardar Contacto'));
    await tester.pumpAndSettle();

    // Ir a lista
    await tester.tap(find.widgetWithText(ElevatedButton, 'Ver Lista de Contactos'));
    await tester.pumpAndSettle();

    // Buscar "Maria"
    await tester.enterText(find.byType(TextField), 'Maria');
    await tester.pump();

    expect(find.text('Maria: 987654321'), findsOneWidget);
  });

  testWidgets('Eliminar contacto con swipe', (WidgetTester tester) async {
    await tester.pumpWidget(const MiAplicacion());

    // Guardar un contacto
    await tester.enterText(find.widgetWithText(TextFormField, 'Ingresa tu nombre'), 'Carlos');
    await tester.enterText(find.widgetWithText(TextFormField, 'Ingresa tu teléfono'), '555555555');
    await tester.tap(find.widgetWithText(ElevatedButton, 'Guardar Contacto'));
    await tester.pumpAndSettle();

    // Ir a lista
    await tester.tap(find.widgetWithText(ElevatedButton, 'Ver Lista de Contactos'));
    await tester.pumpAndSettle();

    // Swipe para eliminar
    await tester.drag(find.text('Carlos: 555555555'), const Offset(-500.0, 0.0));
    await tester.pumpAndSettle();

    // Verifica que se eliminó
    expect(find.text('Carlos: 555555555'), findsNothing);
  });
}
