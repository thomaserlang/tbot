import { Branded } from '@/utils/brand'
import { Command, CommandCreate } from '../../command/types/command.types'

export type CommandTemplateId = Branded<string, 'CommandTemplateId'>

export interface CommandTemplate {
    id: CommandTemplateId
    title: string
    commands: Command[]
    createdAt: string
    updatedAt: string | null
}

export interface CommandTemplateCreate {
    title: string
    commands: CommandCreate[]
}

export interface CommandTemplateUpdate {
    title?: string
    commands?: CommandCreate[]
}
