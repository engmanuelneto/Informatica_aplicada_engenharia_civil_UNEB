from typing import List
from elementos import ElementoEstrutural


class CadastroEstrutural:
    """Gerencia o acervo de elementos estruturais cadastrados."""

    def __init__(self, responsavel: str) -> None:
        self.responsavel = responsavel
        self._elementos: List[ElementoEstrutural] = []

    def adicionar(self, elemento: ElementoEstrutural) -> None:
        self._elementos.append(elemento)

    def listar_resumo(self) -> None:
        print(f"=== RESUMO DO CADASTRO ({self.responsavel}) ===")
        for idx, elem in enumerate(self._elementos, start=1):
            print(f"{idx}. {elem}")

    def exibir_detalhes(self) -> None:
        print("\n=== DETALHAMENTO TÉCNICO DOS ELEMENTOS ===")
        for elem in self._elementos:
            print("-" * 60)
            print(elem.descrever())

    def volume_total_m3(self) -> float:
        return sum(elem.calcular_volume() for elem in self._elementos)

    def peso_proprio_total_kn(self) -> float:
        return sum(elem.calcular_peso_kn() for elem in self._elementos)