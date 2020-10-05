import click


@click.group(invoke_without_command=True)
@click.pass_context
def dfs(ctx):
    """ Root command for distributed file system CLI """
    if ctx.invoked_subcommand is None:
        click.echo('Invoked \'dfs\'!')


@dfs.command(name='init')
def dfs_init():
    """
    Initialize the client storage on a new system,
    should remove any existing file in the dfs root
    directory and return available size.
    """
    click.echo('Invoked \'dfs init\'!')


@dfs.group(name='file', invoke_without_command=True)
@click.pass_context
def dfs_file(ctx):
    if ctx.invoked_subcommand is None:
        click.echo('Invoked \'dfs file\'!')


@dfs_file.command(name='create')
@click.argument('filename', type=click.Path())
def dfs_file_create(filename):
    """
    Should allow to create a new empty file.
    """
    click.echo(f'Invoked \'dfs file create\' with {click.format_filename(filename)}!')


@dfs_file.command(name='read')
@click.argument('filename', type=click.Path())
def dfs_file_read(filename):
    """
    Should allow to read any file from DFS (download a file from the DFS to the Client side).
    """
    click.echo(f'Invoked \'dfs file read\' with {click.format_filename(filename)}!')


@dfs_file.command(name='write')
@click.argument('filename', type=click.Path(exists=True))
def dfs_file_write(filename):
    """
    Should allow to put any file to DFS (upload a file from the Client side to the DFS)
    """
    click.echo(f'Invoked \'dfs file write\' with {click.format_filename(filename)}!')


@dfs_file.command(name='delete')
@click.argument('filename', type=click.Path())
def dfs_file_delete(filename):
    """
    Should allow to delete any file from DFS
    """
    click.echo(f'Invoked \'dfs file delete\' with {click.format_filename(filename)}!')


@dfs_file.command(name='info')
@click.argument('filename', type=click.Path())
def dfs_file_info(filename):
    """
    Should provide information about the file (any useful information - size, node id, etc.)
    """
    click.echo(f'Invoked \'dfs file info\' with {click.format_filename(filename)}!')


@dfs_file.command(name='copy')
@click.argument('filename', type=click.Path())
@click.argument('dest', type=click.Path())
def dfs_file_copy(filename, dest):
    """
    Should allow to create a copy of file.
    """
    click.echo(f'Invoked \'dfs file copy\' with {click.format_filename(filename)} and '
               f'{click.format_filename(dest)}!')


@dfs_file.command(name='move')
@click.argument('filename', type=click.Path())
@click.argument('dest', type=click.Path())
def dfs_file_move(filename, dest):
    """
    Should allow to move a file to the specified path.
    """
    click.echo(f'Invoked \'dfs file move\' with'
               f' {click.format_filename(filename)} and '
               f' {click.format_filename(dest)}!')


@dfs.group(name='dir', invoke_without_command=True)
@click.pass_context
def dfs_dir(ctx):
    if ctx.invoked_subcommand is None:
        click.echo('Invoked \'dfs dir\'!')


@dfs_dir.command(name='open')
@click.argument('name', type=click.Path())
def dfs_dir_open(name):
    """
    Should allow to change directory
    """
    click.echo(f'Invoked \'dfs dir open\' with'
               f' {click.format_filename(name)}!')


@dfs_dir.command(name='read')
@click.argument('name', type=click.Path())
def dfs_dir_read(name):
    """
    Should return list of files, which are stored in the directory.
    """
    click.echo(f'Invoked \'dfs dir read\' with'
               f' {click.format_filename(name)}!')


@dfs_dir.command(name='make')
@click.argument('name', type=click.Path())
def dfs_dir_make(name):
    """
    Should allow to create a new directory.
    """
    click.echo(f'Invoked \'dfs dir make\' with'
               f' {click.format_filename(name)}!')


@dfs_dir.command(name='delete')
@click.argument('name', type=click.Path())
def dfs_dir_delete(name):
    """
    Should allow to delete directory.  If the directory contains
    files the system should ask for confirmation from the
    user before deletion.
    """
    click.echo(f'Invoked \'dfs dir delete\' with'
               f' {click.format_filename(name)}!')
