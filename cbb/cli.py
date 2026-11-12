"""
CLI Command Line Interface for Basquete BR — Atlas Tático.
"""
import sys
import argparse
from pathlib import Path
from cbb.export.html_dashboard import export_dashboard
from cbb.extractors.cbb_archive import CBBArchiveExtractor
from cbb.extractors.cbi_observed import refresh_snapshot as refresh_cbi_snapshot
from cbb.extractors.lnb_observed import refresh_snapshot as refresh_lnb_snapshot
from cbb.database.repository import default_repo

def main():
    parser = argparse.ArgumentParser(description="Basquete BR — Atlas Tático CLI")
    subparsers = parser.add_subparsers(dest="command", help="Comando para executar")
    
    # export
    subparsers.add_parser("export", help="Compilar e exportar HTML estático e JSON para docs/")
    
    # sync
    subparsers.add_parser("sync", help="Coletar dados da CBB e sincronizar com DuckDB")
    
    # server
    server_parser = subparsers.add_parser("server", help="Iniciar servidor local FastAPI")
    server_parser.add_argument("--host", default="127.0.0.1", help="Host")
    server_parser.add_argument("--port", type=int, default=8000, help="Porta")

    args = parser.parse_args()

    if args.command == "export" or args.command is None:
        print("Compilando dados analíticos e exportando dashboard estático...")
        export_dashboard()
    elif args.command == "sync":
        print("Iniciando coleta e sincronização com CBB Archive...")
        try:
            ext = CBBArchiveExtractor()
            teams = ext.fetch_teams()
            hall = ext.fetch_hall_athletes()
            print(f"Coletados: {len(teams)} clubes e {len(hall)} atletas do Hall da Fama.")
            default_repo.log_audit("cbb_archive_sync", len(teams) + len(hall), {"teams": len(teams), "hall": len(hall)})
        except Exception as error:
            print(f"Aviso: arquivo CBB indisponível ({error}).")
        try:
            lnb = refresh_lnb_snapshot()
            print(f"LNB: {lnb['coverage']['games']} jogos; {lnb['coverage']['reports_checked']} relatórios consultados.")
        except Exception as error:
            print(f"Aviso: atualização de NBB/LDB indisponível; snapshot existente preservado ({error}).")
        try:
            cbi = refresh_cbi_snapshot()
            game_count = sum(len(competition["games"]) for competition in cbi["competitions"])
            print(f"CBI/Go Champs: {len(cbi['competitions'])} competições e {game_count} jogos coletados.")
        except Exception as error:
            print(f"Aviso: atualização de CBI indisponível; snapshot existente preservado ({error}).")
        print("Atualizando exportações estáticas...")
        export_dashboard()
    elif args.command == "server":
        import uvicorn
        print(f"Iniciando servidor local em http://{args.host}:{args.port} ...")
        uvicorn.run("cbb.server:app", host=args.host, port=args.port, reload=False)
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
