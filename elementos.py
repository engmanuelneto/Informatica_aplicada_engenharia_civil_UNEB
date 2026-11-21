from abc import ABC, abstractmethod


class ElementoEstrutural(ABC):
    """Classe base abstrata para representação de elementos estruturais de uma edificação."""

    DENSIDADE_CONCRETO_KG_M3 = 2500.0
    PESO_ESPECIFICO_CONCRETO_KN_M3 = 25.0

    def __init__(
        self,
        identificacao: str,
        pavimento: str,
        fck_mpa: float,
        comprimento_m: float,
    ) -> None:
        self.identificacao = identificacao
        self.pavimento = pavimento
        self.fck_mpa = fck_mpa
        self.comprimento_m = comprimento_m

    @abstractmethod
    def calcular_area_secao(self) -> float:
        """Retorna a área da seção transversal ou área em planta (m²)."""

    def calcular_volume(self) -> float:
        """Retorna o volume geométrico do elemento estrutural (m³)."""
        return self.calcular_area_secao() * self.comprimento_m

    def calcular_massa_kg(self) -> float:
        """Estima a massa própria do elemento em concreto armado (kg)."""
        return self.calcular_volume() * self.DENSIDADE_CONCRETO_KG_M3

    def calcular_peso_kn(self) -> float:
        """Estima o peso próprio do elemento em kN."""
        return self.calcular_volume() * self.PESO_ESPECIFICO_CONCRETO_KN_M3

    @abstractmethod
    def descrever(self) -> str:
        """Retorna uma descrição técnica detalhada do elemento estrutural."""

    def __str__(self) -> str:
        return (
            f"[{self.__class__.__name__}] {self.identificacao} | "
            f"Pav.: {self.pavimento} | fck: {self.fck_mpa:.1f} MPa | "
            f"Vol.: {self.calcular_volume():.3f} m³"
        )


class Pilar(ElementoEstrutural):
    """Elemento estrutural vertical submetido predominantemente a compressão."""

    def __init__(
        self,
        identificacao: str,
        pavimento: str,
        fck_mpa: float,
        altura_m: float,
        largura_b_m: float,
        profundidade_h_m: float,
        carga_axial_kn: float,
    ) -> None:
        super().__init__(
            identificacao=identificacao,
            pavimento=pavimento,
            fck_mpa=fck_mpa,
            comprimento_m=altura_m,
        )
        self.largura_b_m = largura_b_m
        self.profundidade_h_m = profundidade_h_m
        self.carga_axial_kn = carga_axial_kn

    @property
    def altura_m(self) -> float:
        return self.comprimento_m

    def calcular_area_secao(self) -> float:
        return self.largura_b_m * self.profundidade_h_m

    def tensao_compressao_media_mpa(self) -> float:
        """Calcula a tensão média de compressão axial estimada (N / A) em MPa."""
        area_m2 = self.calcular_area_secao()
        if area_m2 <= 0:
            return 0.0
        # 1 kN/m² = 0.001 MPa
        return (self.carga_axial_kn / area_m2) * 0.001

    def descrever(self) -> str:
        area = self.calcular_area_secao()
        vol = self.calcular_volume()
        peso = self.calcular_peso_kn()
        tensao = self.tensao_compressao_media_mpa()
        return (
            f"Elemento: Pilar ({self.identificacao})\n"
            f"  Pavimento: {self.pavimento} | fck: {self.fck_mpa:.1f} MPa\n"
            f"  Geometria: b = {self.largura_b_m:.2f} m, h = {self.profundidade_h_m:.2f} m, "
            f"Pé-direito/Altura = {self.altura_m:.2f} m\n"
            f"  Área da seção: {area:.4f} m² | Volume: {vol:.4f} m³ | Peso próprio: {peso:.2f} kN\n"
            f"  Carga axial solicitante: {self.carga_axial_kn:.1f} kN | "
            f"Tensão média (N/A): {tensao:.2f} MPa"
        )


class Viga(ElementoEstrutural):
    """Elemento estrutural linear horizontal submetido à flexão e ao cisalhamento."""

    def __init__(
        self,
        identificacao: str,
        pavimento: str,
        fck_mpa: float,
        vao_m: float,
        largura_bw_m: float,
        altura_h_m: float,
        carga_distribuida_kn_m: float,
    ) -> None:
        super().__init__(
            identificacao=identificacao,
            pavimento=pavimento,
            fck_mpa=fck_mpa,
            comprimento_m=vao_m,
        )
        self.largura_bw_m = largura_bw_m
        self.altura_h_m = altura_h_m
        self.carga_distribuida_kn_m = carga_distribuida_kn_m

    @property
    def vao_m(self) -> float:
        return self.comprimento_m

    def calcular_area_secao(self) -> float:
        return self.largura_bw_m * self.altura_h_m

    def momento_fletor_max_biapoiada_knm(self) -> float:
        """Estima o momento fletor máximo para viga biapoiada sob carga uniforme (q * L² / 8)."""
        return (self.carga_distribuida_kn_m * (self.vao_m ** 2)) / 8.0

    def cortante_max_biapoiada_kn(self) -> float:
        """Estima o esforço cortante máximo para viga biapoiada sob carga uniforme (q * L / 2)."""
        return (self.carga_distribuida_kn_m * self.vao_m) / 2.0

    def descrever(self) -> str:
        area = self.calcular_area_secao()
        vol = self.calcular_volume()
        peso = self.calcular_peso_kn()
        momento = self.momento_fletor_max_biapoiada_knm()
        cortante = self.cortante_max_biapoiada_kn()
        return (
            f"Elemento: Viga ({self.identificacao})\n"
            f"  Pavimento: {self.pavimento} | fck: {self.fck_mpa:.1f} MPa\n"
            f"  Geometria: bw = {self.largura_bw_m:.2f} m, h = {self.altura_h_m:.2f} m, "
            f"Vão = {self.vao_m:.2f} m\n"
            f"  Área da seção: {area:.4f} m² | Volume: {vol:.4f} m³ | Peso próprio: {peso:.2f} kN\n"
            f"  Carga linear: {self.carga_distribuida_kn_m:.1f} kN/m | "
            f"Momento máx. (qL²/8): {momento:.2f} kN·m | Cortante máx.: {cortante:.2f} kN"
        )


class Laje(ElementoEstrutural):
    """Elemento estrutural laminar bidimensional (maciça)."""

    def __init__(
        self,
        identificacao: str,
        pavimento: str,
        fck_mpa: float,
        comprimento_lx_m: float,
        largura_ly_m: float,
        espessura_h_m: float,
    ) -> None:
        super().__init__(
            identificacao=identificacao,
            pavimento=pavimento,
            fck_mpa=fck_mpa,
            comprimento_m=comprimento_lx_m,
        )
        self.largura_ly_m = largura_ly_m
        self.espessura_h_m = espessura_h_m

    def calcular_area_secao(self) -> float:
        """Retorna a área em planta da laje (Lx * Ly) em m²."""
        return self.comprimento_m * self.largura_ly_m

    def calcular_volume(self) -> float:
        """Retorna o volume de concreto da laje (Área em planta * espessura) em m³."""
        return self.calcular_area_secao() * self.espessura_h_m

    def descrever(self) -> str:
        area = self.calcular_area_secao()
        vol = self.calcular_volume()
        peso = self.calcular_peso_kn()
        return (
            f"Elemento: Laje Maciça ({self.identificacao})\n"
            f"  Pavimento: {self.pavimento} | fck: {self.fck_mpa:.1f} MPa\n"
            f"  Geometria: Lx = {self.comprimento_m:.2f} m, Ly = {self.largura_ly_m:.2f} m, "
            f"Espessura h = {self.espessura_h_m:.2f} m\n"
            f"  Área em planta: {area:.2f} m² | Volume: {vol:.4f} m³ | Peso próprio: {peso:.2f} kN"
        )