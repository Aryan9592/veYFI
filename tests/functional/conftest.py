import pytest

DAY = 86400
WEEK = 7 * DAY


@pytest.fixture(scope="session")
def gov(accounts):
    yield accounts[0]


@pytest.fixture(scope="session")
def whale_amount():
    yield 10**22


@pytest.fixture(scope="session")
def whale(accounts, yfi, whale_amount):
    a = accounts[1]
    yfi.mint(a, whale_amount, sender=a)
    yield a


@pytest.fixture(scope="session")
def shark_amount():
    yield 10**20


@pytest.fixture(scope="session")
def shark(accounts, yfi, shark_amount):
    a = accounts[2]
    yfi.mint(a, shark_amount, sender=a)
    yield a


@pytest.fixture(scope="session")
def fish_amount():
    yield 10**18


@pytest.fixture(scope="session")
def fish(accounts, yfi, fish_amount):
    a = accounts[3]
    yfi.mint(a, fish_amount, sender=a)
    yield a


@pytest.fixture(scope="session")
def panda(accounts):
    yield accounts[4]


@pytest.fixture(scope="session")
def doggie(accounts):
    yield accounts[5]


@pytest.fixture(scope="session")
def bunny(accounts):
    yield accounts[6]


@pytest.fixture(scope="session")
def yfi(project, gov):
    yield gov.deploy(project.Token, "YFI")


@pytest.fixture(scope="session")
def create_token(project, gov):
    def create_token(name):
        return gov.deploy(project.Token, name)

    yield create_token


@pytest.fixture(scope="session")
def ve_yfi_rewards(ve_yfi_and_reward_pool):
    (_, ve_yfi_rewards) = ve_yfi_and_reward_pool
    yield ve_yfi_rewards


@pytest.fixture(scope="session")
def gauge_factory(project, gov, ve_yfi, o_yfi, ve_yfi_o_yfi_pool):
    gauge = gov.deploy(project.Gauge, ve_yfi, o_yfi, ve_yfi_o_yfi_pool)
    yield gov.deploy(project.GaugeFactory, gauge)


@pytest.fixture(scope="session")
def registry(project, gov, ve_yfi, yfi, gauge_factory, ve_yfi_rewards):
    yield gov.deploy(project.Registry, ve_yfi, yfi, gauge_factory, ve_yfi_rewards)


@pytest.fixture(scope="session")
def create_vault(project, gov):
    def create_vault():
        return gov.deploy(project.Token, "Yearn vault")

    yield create_vault


@pytest.fixture(scope="session")
def create_gauge(registry, gauge_factory, gov, project):
    def create_gauge(vault):
        tx = registry.addVaultToRewards(vault, gov, sender=gov)
        gauge_address = tx.decode_logs(gauge_factory.GaugeCreated)[0].gauge
        return project.Gauge.at(gauge_address)

    yield create_gauge
