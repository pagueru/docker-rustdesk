import json
import subprocess
from pathlib import Path
from typing import Any, Dict, List, Union

from core.constants import JSON_FILE, OUTPUT_PATH, PROJECT_PATH, SCRIPTS_PATH
from core.utils import logger, start_config

# Configurações globais
ADD_BAT_FILE = SCRIPTS_PATH / "add_firewall_rules.bat"
VERIFY_BAT_FILE = SCRIPTS_PATH / "verify_firewall_rules.bat"
DELETE_BAT_FILE = SCRIPTS_PATH / "delete_firewall_rules.bat"
OUTPUT_TXT_FILE = OUTPUT_PATH / "firewall_rules_verification.txt"


def rpath(input_path: Union[Path, str]) -> str:
    """
    Retorna o caminho relativo ao projeto definido por PROJECT_PATH.

    Args:
        input_path (Union[Path, str]): Caminho absoluto ou relativo a ser processado.

    Returns:
        str: Caminho relativo ao PROJECT_PATH.
    """
    return str(Path(input_path).relative_to(PROJECT_PATH))


def load_rules_from_json(json_file: Path) -> List[Dict[str, Any]]:
    """
    Carrega as regras de firewall de um arquivo JSON.

    Args:
        json_file (Path): Caminho para o arquivo JSON contendo as regras de firewall.

    Returns:
        List[Dict[str, Any]]: Lista de dicionários representando as regras de firewall.

    Raises:
        RuntimeError: Se ocorrer um erro ao carregar o arquivo JSON.
    """
    try:
        # Carrega as regras do arquivo JSON
        with json_file.open("r", encoding="utf-8") as file:
            rules = json.load(file)
            logger.info(f"Arquivo JSON '{rpath(json_file)}' carregado com sucesso.")
            return rules
    except Exception as e:
        logger.error(
            f"Erro ao carregar as regras do arquivo JSON '{rpath(json_file)}': {e}"
        )
        raise RuntimeError from e


def create_add_rules_bat(rules: List[Dict[str, str]], bat_file_name: Path) -> int:
    """
    Cria um arquivo .bat para adicionar regras de firewall.

    Args:
        rules (List[Dict[str, str]]): Lista de regras de firewall a serem adicionadas.
        bat_file_name (Path): Caminho do arquivo .bat a ser criado.

    Returns:
        int: Número de regras de firewall adicionadas ao arquivo .bat.

    Raises:
        RuntimeError: Erro ao criar o arquivo .bat.
    """
    try:
        # Itera sobre cada regra de firewall fornecida
        with bat_file_name.open("w", encoding="utf-8") as bat_file:
            for rule in rules:
                rule_name: str = rule["name"]
                rule_port: str = rule["port"]
                rule_protocol: str = rule["protocol"]

                # Cria a linha de comando para adicionar a regra de firewall
                line: str = (
                    f'netsh advfirewall firewall add rule name="{rule_name}" '
                    f"dir=in action=allow protocol={rule_protocol} localport={rule_port} "
                    f"remoteip=any profile=any\n"
                )

                # Adiciona a linha de comando ao arquivo .bat
                bat_file.write(line)
            bat_file.write("pause")
        logger.info(f"Arquivo .bat '{rpath(bat_file_name)}' criado com sucesso.")
        return len(rules)
    except Exception as e:
        logger.error(f"Erro ao criar arquivo .bat '{rpath(bat_file_name)}': {e}")
        raise RuntimeError from e


def create_delete_rules_bat(rules: List[Dict[str, str]], bat_file_name: Path) -> int:
    try:
        # Itera sobre cada regra de firewall fornecida
        with bat_file_name.open("w", encoding="utf-8") as bat_file:
            for rule in rules:
                rule_name: str = rule["name"]

                # Cria a linha de comando para adicionar a regra de firewall
                line: str = (
                    f'netsh advfirewall firewall delete rule name="{rule_name}"\n'
                )

                # Adiciona a linha de comando ao arquivo .bat
                bat_file.write(line)
            bat_file.write("pause")
        logger.info(f"Arquivo .bat '{rpath(bat_file_name)}' criado com sucesso.")
        return len(rules)
    except Exception as e:
        logger.error(f"Erro ao criar arquivo .bat '{rpath(bat_file_name)}': {e}")
        raise RuntimeError from e


def verify_rules_in_terminal(rules: List[Dict[str, str]]) -> str:
    """
    Verifica se as regras de firewall existem no terminal.

    Args:
        rules (List[Dict[str, str]]): Lista de regras de firewall a serem verificadas.

    Returns:
        str: Resultado da verificação de regras de firewall no terminal.
    """

    # Inicializa lista para armazenar resultados
    results: List[str] = []

    try:
        # Itera sobre as regras de firewall
        for rule in rules:
            rule_name: str = rule["name"]  # Nome da regra

            # Comando para verificar a existencia da regra
            command: str = f'netsh advfirewall firewall show rule name="{rule_name}"'

            # Executa o comando e captura a saída
            result: subprocess.CompletedProcess[str] = subprocess.run(
                command,
                shell=True,
                capture_output=True,  # Captura a saída do comando
                text=True,  # Interpreta a saída como texto
                check=False,  # Verifica se o comando foi executado com sucesso
            )

            # Adiciona a saída do comando à lista de resultados
            results.append(result.stdout or result.stderr)

            # Verifica se a regra foi encontrada
            if (
                "Nenhuma regra correspondente aos critérios especificados."
                in result.stdout
            ):
                logger.info(f"Regra encontrada: '{rule_name}'")

            if "Ok." in result.stdout:
                logger.info(f"Regra não encontrada: '{rule_name}'.")

        logger.info("Verificação de regras no terminal concluída com sucesso.")
        return "\n".join(results)

    except Exception as e:
        logger.error(f"Erro ao verificar regras no terminal: {e}")
        raise RuntimeError from e


def save_verification_to_file(verification_result: str, output_file: Path) -> None:
    """
    Salva o resultado da verificação de regras de firewall em um arquivo de texto.

    Args:
        verification_result (str): Resultado da verificação de regras de firewall.
        output_file (Path): Caminho do arquivo de texto para salvar o resultado.

    Returns:
        None

    Raises:
        RuntimeError: Erro ao salvar verificação em '{output_file}': {e}
    """
    try:
        # Escreve o resultado da verificação no arquivo
        with output_file.open("w", encoding="utf-8") as file:
            file.write(verification_result)
        logger.info(f"Resultado da verificação salvo em '{rpath(output_file)}'.")
    except Exception as e:
        logger.error(f"Erro ao salvar verificação em '{rpath(output_file)}': {e}")
        raise RuntimeError from e


def create_verify_rules_bat(
    rules: List[Dict[str, str]], verify_bat_file_name: Path
) -> None:
    """
    Cria um arquivo .bat para verificar se as regras de firewall existem no
    terminal e salva o resultado em um arquivo de texto.

    Args:
        rules (List[Dict[str, str]]): Lista de regras de firewall.
        verify_bat_file_name (Path): Caminho do arquivo .bat a ser criado.
        output_file (Path): Caminho do arquivo de texto para salvar o resultado.
    """
    try:
        # Cria uma linha dex comando para cada regra
        with verify_bat_file_name.open("w", encoding="utf-8") as bat_file:
            for rule in rules:
                rule_name = rule["name"]
                bat_file.write(
                    f'netsh advfirewall firewall show rule name="{rule_name}"\n'
                )
            bat_file.write("pause")
        logger.info(f"Arquivo .bat '{rpath(verify_bat_file_name)}' criado com sucesso.")

    except Exception as e:
        logger.error(f"Erro ao criar arquivo .bat '{rpath(verify_bat_file_name)}': {e}")
        raise RuntimeError from e


def main() -> None:
    """
    Função principal para execução do script.
    """
    try:
        # Inicializa o logger e limpa a tela
        start_config()

        # Verifica se o diretório de scripts existe e o cria se necessário
        if not SCRIPTS_PATH.exists():
            SCRIPTS_PATH.mkdir(parents=True)

        # Carrega as regras de firewall do arquivo JSON
        rules: List[Dict[str, str]] = load_rules_from_json(JSON_FILE)

        # Verifica se alguma regra foi encontrada
        if not rules:
            logger.error("Nenhuma regra encontrada no arquivo JSON.")
            return

        # Mostra o número de regras encontradas
        logger.info(f"{len(rules)} regra(s) encontrada(s). Gerando arquivos .bat.")

        # Gera um arquivo .bat para adicionar as regras de firewall
        create_add_rules_bat(rules, ADD_BAT_FILE)

        # Gera um arquivo .bat para verificar as regras de firewall
        create_verify_rules_bat(rules, VERIFY_BAT_FILE)

        # Gera um arquivo .bat para excluir as regras de firewall
        create_delete_rules_bat(rules, DELETE_BAT_FILE)

        # Verifica se as regras de firewall existem no terminal
        if VERIFY_BAT_FILE.exists():
            verification_result = verify_rules_in_terminal(rules)

            # Salva o resultado da verificação em um arquivo de texto
            save_verification_to_file(verification_result, OUTPUT_TXT_FILE)

        else:
            logger.error(f"Arquivo de saída '{OUTPUT_TXT_FILE}' não encontrado.")

    except RuntimeError as e:
        logger.error(f"Erro inesperado durante a execução: {e}")


if __name__ == "__main__":
    main()
