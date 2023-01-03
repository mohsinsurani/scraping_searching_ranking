import 'dart:convert';

import 'package:flutter/material.dart';
import 'package:http/http.dart' as http;
import 'package:url_launcher/url_launcher.dart';

void main() {
  runApp(const MyApp());
}

class MyApp extends StatelessWidget {
  const MyApp({Key? key}) : super(key: key);

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      debugShowCheckedModeBanner: false,
      title: 'SEFA Publications',
      theme: ThemeData(
        primarySwatch: Colors.blue,
      ),
      home: const MyHomePage(title: 'Flutter Demo Home Page'),
    );
  }
}

class MyHomePage extends StatefulWidget {
  const MyHomePage({Key? key, required this.title}) : super(key: key);
  final String title;

  @override
  State<MyHomePage> createState() => _MyHomePageState();
}

class _MyHomePageState extends State<MyHomePage> {
  String titleSt = "0";
  final TextEditingController _searchController =
      TextEditingController(text: "");
  List<dynamic>? pub_list;

  @override
  void initState() {
    super.initState();
  }

  void _incrementCounter() async {
    const url = 'http://127.0.0.1:5001/search';
    final urli = Uri.parse(url);
    final resp = await http.post(urli,
        body: json.encode({'query': _searchController.text}),
        headers: {'Accept': '*/*'});

    pub_list = jsonDecode(resp.body);
    titleSt = pub_list![1]["pub_title"];
    setState(() {});
    print(pub_list);
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        // title: Text(titleSt),
        title: const Text("Search your favorite SEFA publication"),
      ),
      body: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        mainAxisAlignment: MainAxisAlignment.start,
        children: [
          Row(
            children: <Widget>[
              SizedBox(
                width: MediaQuery.of(context).size.width - 350,
                height: 40,
                child: TextField(
                  controller: _searchController,
                  decoration: const InputDecoration(
                    hintText: 'Search your favourite publication',
                    contentPadding: EdgeInsets.all(10.0),
                  ),
                  style: TextStyle(),
                  onChanged: (value) {},
                ),
              ),
              FloatingActionButton(
                onPressed: _incrementCounter,
                tooltip: 'Search',
                child: const Icon(Icons.search),
              ),
            ],
          ),
          Expanded(
            child: ListView.separated(
              shrinkWrap: true,
              itemCount: pub_list?.length ?? 0,
              separatorBuilder: (_, __) => const Divider(),
              itemBuilder: (context, int index) {
                final pubTitle = pub_list![index]["pub_title"];
                final authName = pub_list![index]["auth_name"];
                final pubDate = pub_list![index]["pub_date"];
                final pubLink = pub_list![index]["pub_link"];
                print("title is $pubTitle");

                return ListTile(
                  title: InkWell(
                    onTap: () async {
                      await launchUrl(Uri.parse(pubLink));
                    },
                    hoverColor: Colors.grey.shade200,
                    child: Text(
                      '$pubTitle',
                      textScaleFactor: 1.1,
                      textWidthBasis: TextWidthBasis.longestLine,
                      // style: ,
                    ),
                  ),
                  subtitle: InkWell(
                    child: Text(
                      "$authName - School of Economics, Finance and Accounting, ${pubDate.toUpperCase()} - pureportal.coventry.ac.uk",
                      textWidthBasis: TextWidthBasis.longestLine,
                    ),
                  ),
                );
              },
            ),
          )
        ],
      ),
    );
  }
}
