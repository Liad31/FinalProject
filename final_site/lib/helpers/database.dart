import 'package:mongo_dart/mongo_dart.dart';

class MongoDatabase {
  static var db;
  static var userCollection;
  static bool open = false;

  static connect() async {
    if (!open) {
      db = await Db.create(
          "mongodb+srv://ourProject:EMGwk59xADuSIIkv@cluster0.lhfaj.mongodb.net/production3?retryWrites=true&w=majority");
      print(1);
      await db.open();
      print(2);
      userCollection = db.collection('tiktokusernationalistics');
      open = true;
    }
  }

  static List<Map<String, dynamic>> getDocuments() {
    try {
      final users = userCollection.find().toList();
      print(users);
      return users;
    } catch (e) {
      print(e);
      return [];
    }
  }
}
