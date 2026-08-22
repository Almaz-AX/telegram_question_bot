import 'dart:convert';
import 'dart:io';
import 'package:http/http.dart' as http;

// Переменные окружения: Render передаст их при запуске
final String botToken = Platform.environment['BOT_TOKEN'] ?? '';
final int adminChatId = int.parse(Platform.environment['ADMIN_CHAT_ID'] ?? '0');

Future<void> main() async {
  if (botToken.isEmpty) {
    print('Ошибка: не задан BOT_TOKEN');
    exit(1);
  }
  if (adminChatId == 0) {
    print('Ошибка: не задан ADMIN_CHAT_ID');
    exit(1);
  }

  final server = await HttpServer.bind(InternetAddress.anyIPv4, 8080);
  print('Server running on port 8080');

  await for (var request in server) {
    if (request.method == 'POST' && request.uri.path == '/webhook') {
      String bodyString = await request.cast<List<int>>().transform(utf8.decoder).join();
      final body = jsonDecode(bodyString) as Map<dynamic, dynamic>;

      final message = body['message'];
      if (message != null) {
        final text = message['text'];
        if (text != null) {
          final date = message['date'] as int;
          final timeStr = DateTime.fromMillisecondsSinceEpoch(date * 1000)
              .toLocal()
              .toString()
              .split('.')[0];

          // Пересылаем вопрос тебе в канал
          await sendMessage(
            adminChatId,
            '📬 Анонимный вопрос ($timeStr)\n\n$text',
          );

          // Отвечаем пользователю
          final chatId = (message['chat'] as Map)['id'];
          await sendMessage(
            chatId,
            'Спасибо, вопрос принят. Разберу на этой неделе.',
          );
        }
      }

      request.response
        ..statusCode = 200
        ..write(jsonEncode({'ok': true}))
        ..close();
    } else {
      request.response
        ..statusCode = 404
        ..write('Not found')
        ..close();
    }
  }
}

Future<void> sendMessage(int chatId, String text) async {
  await http.post(
    Uri.parse('https://api.telegram.org/bot$botToken/sendMessage'),
    headers: {'Content-Type': 'application/json'},
    body: jsonEncode({
      'chat_id': chatId,
      'text': text,
    }),
  );
}
