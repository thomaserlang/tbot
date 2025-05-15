import {
    Box,
    Button,
    Container,
    Flex,
    Grid,
    Image,
    SimpleGrid,
    Text,
    ThemeIcon,
    Title,
} from '@mantine/core'
import {
    IconCommand,
    IconMessage,
    IconRobot,
    IconShield,
} from '@tabler/icons-react'
import { Link } from 'react-router-dom'
import classes from './landing.page.module.css'

const features = [
    {
        icon: IconRobot,
        title: 'Your own bot name',
        description:
            "Connect your own bot's Twitch/YouTube account to use your own custom bot name",
    },
    {
        icon: IconShield,
        title: 'Chat Filter',
        description: 'Protect all your chats with simple filters in one place',
    },
    {
        icon: IconMessage,
        title: 'Combined Chat',
        description:
            'Simply connect your accounts and have all your chats combined in one place.',
    },
    {
        icon: IconCommand,
        title: 'Commands/Timers',
        description:
            'Let your viewers know what you are listening to on Spotify or anything else relevant. Create it once and have it work in all of your chats',
    },
]

export function Component() {
    const items = features.map((feature) => (
        <div key={feature.title}>
            <ThemeIcon
                size={44}
                radius="md"
                variant="gradient"
                gradient={{ deg: 133, from: 'blue', to: 'cyan' }}
            >
                <feature.icon size={26} stroke={1.5} />
            </ThemeIcon>
            <Text fz="lg" mt="sm" fw={500}>
                {feature.title}
            </Text>
            <Text c="dimmed" fz="sm">
                {feature.description}
            </Text>
        </div>
    ))

    return (
        <>
            <title>Synchra - Multiplatform Streaming Tools</title>
            <meta
                name="description"
                content="A set of tools to help you manage your stream on
                                multiple platforms in one place. With a focus on
                                simplicity and ease of use."
            />
            <meta
                name="keywords"
                content="Multiplartform streaming, Your own bot name, Combined Chat, Chat Filter, Commands/Timers"
            />
            <Container size="lg">
                <div className={classes.wrapper}>
                    <Grid gutter={80}>
                        <Grid.Col span={{ base: 12, md: 6 }}>
                            <Flex
                                gap="0.5rem"
                                wrap={'wrap'}
                                justify="center"
                                align="center"
                                mb="1rem"
                            >
                                <Flex direction="column">
                                    <Image
                                        ml="-0.15rem"
                                        src="/logo.svg"
                                        alt="Synchra"
                                        w={300}
                                    />
                                    <Text
                                        c="dimmed"
                                        mt="-1.5rem"
                                        fw={500}
                                        fz={25}
                                    >
                                        Work smarter, not harder
                                    </Text>
                                </Flex>
                                <Box mt="0.25rem">
                                    <Image
                                        src="/tree.svg"
                                        alt="Synchra"
                                        w={150}
                                    />
                                </Box>
                            </Flex>
                        </Grid.Col>
                    </Grid>

                    <Grid gutter={80}>
                        <Grid.Col span={{ base: 12, md: 5 }}>
                            <Title className={classes.title} order={2}>
                                Multiplatform streaming tools
                            </Title>
                            <Text c="dimmed">
                                A set of tools to help you manage your stream on
                                multiple platforms in one place. With a focus on
                                simplicity and ease of use.
                                <br />
                                <br />
                                Twitch, YouTube and TikTok support and more to
                                come.
                            </Text>

                            <Button
                                component={Link}
                                to="/channels"
                                variant="gradient"
                                gradient={{
                                    deg: 133,
                                    from: 'blue',
                                    to: 'cyan',
                                }}
                                size="lg"
                                radius="md"
                                mt="xl"
                            >
                                Dashboard
                            </Button>
                        </Grid.Col>
                        <Grid.Col span={{ base: 12, md: 7 }}>
                            <SimpleGrid cols={{ base: 1, md: 2 }} spacing={30}>
                                {items}
                            </SimpleGrid>
                        </Grid.Col>
                    </Grid>
                </div>
            </Container>
        </>
    )
}
