import json
import glob
import os

pokemon_data = []

for arquivo in glob.glob("*.json"):
    try:
        nome_arquivo = os.path.splitext(os.path.basename(arquivo))[0]
        partes = nome_arquivo.split("_", 1)

        if len(partes) != 2:
            continue

        numero_dex = partes[0]
        nome_arquivo_pokemon = partes[1].lower()

        with open(arquivo, "r", encoding="utf-8") as f:
            dados = json.load(f)

        for spawn in dados.get("spawns", []):
            condition = spawn.get("condition", {})

            biomes = condition.get("biomes", [])
            biomes = [
                bioma.split("is_", 1)[-1].split(":", 1)[-1]
                for bioma in biomes
            ]

            nearby_blocks = condition.get("neededNearbyBlocks", [])
            nearby_blocks = [
                bloco.split(":", 1)[-1]
                for bloco in nearby_blocks
            ]

            pokemon_data.append({
                "pokemon": spawn.get("pokemon", nome_arquivo_pokemon),
                "numero": numero_dex,
                "position": spawn.get("spawnablePositionType", "N/A"),
                "bucket": spawn.get("bucket", "N/A"),
                "weight": spawn.get("weight", "N/A"),
                "level": spawn.get("level", "N/A"),
                "biomes": biomes,
                "nearby_blocks": nearby_blocks,
                "min_sky": condition.get("minSkyLight", "N/A"),
                "max_sky": condition.get("maxSkyLight", "N/A")
            })

    except (json.JSONDecodeError, OSError, ValueError):
        continue


while True:
    pesquisa = input(
        "\nDigite o nome ou número da Pokédex (ou 'sair' OBS: ' ' exibe todos os 1024 registros da pokedex): "
    ).strip().lower()

    if pesquisa == "sair":
        print("Programa encerrado.")
        break

    if pesquisa == "":
        resultados = pokemon_data
    else:
        resultados = [
            spawn for spawn in pokemon_data
            if pesquisa in spawn["pokemon"].lower()
            or pesquisa in spawn["numero"]
        ]

    if not resultados:
        print("Nenhum Pokémon encontrado.")
        continue

    for spawn in resultados:
        print("\n" + "=" * 50)
        print(f"Pokémon: {spawn['pokemon']}")
        print(f"Pokédex: {spawn['numero']}")
        print(f"Posição: {spawn['position']}")
        print(f"Bucket: {spawn['bucket']}")
        print(f"Peso: {spawn['weight']}")
        print(f"Nível: {spawn['level']}")
        print(f"Biomas: {', '.join(spawn['biomes']) or 'N/A'}")
        print(
            f"Blocos próximos: "
            f"{', '.join(spawn['nearby_blocks']) or 'N/A'}"
        )
        print(f"Min Sky Light: {spawn['min_sky']}")
        print(f"Max Sky Light: {spawn['max_sky']}")