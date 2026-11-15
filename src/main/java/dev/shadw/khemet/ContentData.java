package dev.shadw.khemet;

import com.google.gson.JsonObject;
import com.google.gson.JsonParser;
import java.io.IOException;
import java.io.InputStream;
import java.io.InputStreamReader;
import java.nio.charset.StandardCharsets;

/** The numbers for the gods, favor, artifacts and sandstorms, read from assets/khemet/content.json (shared with the site). */
final class ContentData {
	private static JsonObject root;

	private ContentData() {}

	static synchronized JsonObject root() {
		if (root == null) {
			String path = "/assets/" + Mod.MOD_ID + "/content.json";
			try (InputStream stream = ContentData.class.getResourceAsStream(path)) {
				if (stream == null) {
					throw new IllegalStateException("missing " + path);
				}
				root = JsonParser.parseReader(new InputStreamReader(stream, StandardCharsets.UTF_8)).getAsJsonObject();
			} catch (IOException e) {
				throw new IllegalStateException("cannot read " + path, e);
			}
		}
		return root;
	}

	static JsonObject altar(String god) {
		return root().getAsJsonObject("altars").getAsJsonObject(god);
	}

	static double d(String item, String field) {
		return root().getAsJsonObject(item).get(field).getAsDouble();
	}

	static int i(String item, String field) {
		return root().getAsJsonObject(item).get(field).getAsInt();
	}
}
